"""Offline, opt-in OVizLAB Agent Skills installer. Python 3.10+ stdlib only."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys
import uuid

AGENTS = {
    'codex': ('.agents', '.agents'),
    'claude': ('.claude', '.claude'),
    'cursor': ('.cursor', '.cursor'),
    'copilot': ('.copilot', '.github'),
}
NAME_RE = re.compile(r'^[a-z0-9][a-z0-9-]{1,79}$')
SHA_RE = re.compile(r'^[a-f0-9]{64}$')
WINDOWS_RESERVED = frozenset({'CON', 'PRN', 'AUX', 'NUL'} |
                             {'COM' + str(i) for i in range(1, 10)} |
                             {'LPT' + str(i) for i in range(1, 10)})


def checksum(content):
    return hashlib.sha256(content).hexdigest()


def safe_rel(rel):
    # Protect POSIX and Windows layouts against ADS, device names, trailing-dot
    # aliases, ambiguous casefold collisions and path traversal.
    if not isinstance(rel, str) or not 0 < len(rel) < 260 or '\\' in rel:
        return False
    parts = rel.split('/')
    if len(parts) < 3 or parts[0] != 'skills' or not NAME_RE.fullmatch(parts[1]):
        return False
    for part in parts:
        if (part in ('', '.', '..') or part.endswith(('.', ' '))
                or part.split('.')[0].upper() in WINDOWS_RESERVED
                or any(ord(char) < 32 or char in '<>:"|?*' for char in part)):
            return False
    return True

def load_bundle(bundle):
    base = Path(bundle).absolute()
    if not base.is_dir() or base.is_symlink():
        raise ValueError('Bundle must be a local, real directory extracted from the ZIP')
    manifest_file = base / 'bundle.json'
    if manifest_file.is_symlink():
        raise ValueError('Symlinked manifest blocked')
    info = json.loads(manifest_file.read_text(encoding='utf-8'))
    if info.get('schema_version') != 1 or info.get('repository') != 'lutiy-dev/GitHab-Skills':
        raise ValueError('Unexpected bundle provenance/schema')
    if not re.fullmatch(r'[a-f0-9]{40}', info.get('source_commit', '')):
        raise ValueError('Exact source commit missing')
    entries = info.get('files')
    if not isinstance(entries, dict) or not entries or len(entries) > 500:
        raise ValueError('Invalid file inventory')
    if len({rel.casefold() for rel in entries}) != len(entries):
        raise ValueError('Windows case-insensitive path collision in bundle')
    skills = set()
    content = {}
    for rel, meta in entries.items():
        if not safe_rel(rel) or not isinstance(meta, dict) or not SHA_RE.fullmatch(meta.get('sha256', '')):
            raise ValueError('Unsafe manifest path or digest: ' + str(rel))
        if not isinstance(meta.get('bytes'), int) or not 0 <= meta['bytes'] <= 2_000_000:
            raise ValueError('Invalid entry size')
        f = base.joinpath(*rel.split('/'))
        if any(part.is_symlink() for part in [f] + list(f.parents)[:3]):
            raise ValueError('Symlink in package path: ' + rel)
        raw = f.read_bytes()
        if len(raw) != meta['bytes'] or checksum(raw) != meta['sha256']:
            raise ValueError('Bundle integrity failure: ' + rel)
        content[rel] = raw
        skills.add(rel.split('/')[1])
    for skill in skills:
        key = f'skills/{skill}/SKILL.md'
        if key not in content:
            raise ValueError('Skill entry point missing: ' + key)
        first = content[key].decode('utf-8').split('---', 2)
        if len(first) != 3 or first[0] != '' or not re.search(r'^name:\s*' + re.escape(skill) + r'\s*$', first[1], re.M):
            raise ValueError('Skill frontmatter name mismatch: ' + skill)
    if set(info.get('skills', [])) != skills:
        raise ValueError('Manifest skill inventory mismatch')
    return info, content


def target_roots(agents, scope, project_root=None, home=None):
    if scope == 'project' and not project_root:
        raise ValueError('--project-root required for project scope')
    root = Path(project_root).absolute() if scope == 'project' else Path(home or Path.home()).absolute()
    if not root.is_dir() or root.is_symlink():
        raise ValueError('Installation base must be a real existing directory')
    output = []
    for agent in dict.fromkeys(agents):
        if agent not in AGENTS:
            raise ValueError('Unsupported agent: ' + agent)
        dirname = AGENTS[agent][0 if scope == 'user' else 1]
        output.append((agent, root / dirname / 'skills'))
    return output


def current_digest(path):
    if path.is_symlink() or not path.is_dir():
        raise ValueError('Existing skill is not a real directory: ' + str(path))
    files = {}
    for f in path.rglob('*'):
        if f.is_symlink():
            raise ValueError('Existing symlink blocked: ' + str(f))
        if f.is_file():
            files[f.relative_to(path).as_posix()] = checksum(f.read_bytes())
    return files


def desired_digest(content, skill):
    prefix = f'skills/{skill}/'
    return {rel[len(prefix):]: checksum(raw) for rel, raw in content.items() if rel.startswith(prefix)}


def prepare_plan(bundle, agents, scope, project_root=None, home=None, selected=None):
    info, content = load_bundle(bundle)
    roots = target_roots(agents, scope, project_root, home)
    skills = sorted(set(selected or info['skills']))
    if not skills or not set(skills).issubset(info['skills']):
        raise ValueError('Unknown selected skill')
    plan = []
    for agent, root in roots:
        if root.exists() and (root.is_symlink() or not root.is_dir()):
            raise ValueError('Unsafe existing skills root: ' + str(root))
        if root.parent.exists() and root.parent.is_symlink():
            raise ValueError('Symlinked agent configuration blocked')
        for skill in skills:
            dest = root / skill
            expected = desired_digest(content, skill)
            existing = current_digest(dest) if dest.exists() or dest.is_symlink() else None
            plan.append({'agent': agent, 'path': str(dest), 'skill': skill,
                         'action': 'SKIP' if existing == expected else ('BACKUP+REPLACE' if existing is not None else 'INSTALL')})
    return info, content, plan


def execute(bundle, agents, scope, project_root=None, home=None, selected=None):
    info, content, plan = prepare_plan(bundle, agents, scope, project_root, home, selected)
    steps = [p for p in plan if p['action'] != 'SKIP']
    transaction = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S') + '-' + uuid.uuid4().hex[:8]
    records = []
    if not steps:
        return {'status': 'NO_CHANGE', 'source_commit': info['source_commit'], 'plan': plan, 'receipts': []}
    # Commit a complete package into a temporary folder; do not merge files into existing installs.
    try:
        for p in steps:
            dest = Path(p['path']); root = dest.parent
            root.mkdir(parents=True, exist_ok=True)
            if root.is_symlink():
                raise ValueError('Unsafe target root')
            backup_root = root.parent / '.ovizlab-backups' / transaction
            if backup_root.is_symlink():
                raise ValueError('Symlinked backup root blocked')
            backup_root.mkdir(parents=True, exist_ok=True)
            backup = backup_root / p['skill']
            temp = root / ('.ovizlab-stage-' + uuid.uuid4().hex)
            temp.mkdir()
            try:
                for rel, data in content.items():
                    prefix = f'skills/{p["skill"]}/'
                    if rel.startswith(prefix):
                        f = temp.joinpath(*rel[len(prefix):].split('/'))
                        f.parent.mkdir(parents=True, exist_ok=True)
                        f.write_bytes(data)
                # Keep exactly one backup, and never follow links when replacing.
                if dest.exists() or dest.is_symlink():
                    if dest.is_symlink():
                        raise ValueError('Symlinked target blocked')
                    dest.rename(backup)
                    was_existing = True
                else:
                    was_existing = False
                try:
                    temp.rename(dest)
                except Exception:
                    if was_existing:
                        backup.rename(dest)
                    raise
                records.append({'agent': p['agent'], 'skill': p['skill'], 'destination': str(dest),
                                'backup': str(backup) if was_existing else None,
                                'installed_files': desired_digest(content, p['skill']),
                                'receipt_path': str(backup_root / 'receipt.json')})
            finally:
                if temp.exists():
                    shutil.rmtree(temp)
        # One receipt per agent/target transaction; group by backup root.
        grouped = {}
        for record in records:
            grouped.setdefault(record['receipt_path'], []).append({k: v for k, v in record.items() if k != 'receipt_path'})
        for filename, details in grouped.items():
            Path(filename).write_text(json.dumps({'schema_version': 1, 'source_commit': info['source_commit'],
                                                  'records': details}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        return {'status': 'INSTALLED', 'source_commit': info['source_commit'], 'plan': plan,
                'receipts': sorted(grouped)}
    except Exception:
        # Best-effort automatic rollback of changes from this invocation only.
        for record in reversed(records):
            dest = Path(record['destination']); backup = Path(record['backup']) if record['backup'] else None
            if dest.exists() and current_digest(dest) == record['installed_files']:
                shutil.rmtree(dest)
                if backup and backup.exists():
                    backup.rename(dest)
        raise


def rollback(receipt_path):
    file = Path(receipt_path).absolute()
    doc = json.loads(file.read_text(encoding='utf-8'))
    if doc.get('schema_version') != 1 or not isinstance(doc.get('records'), list):
        raise ValueError('Invalid rollback receipt')
    # Receipts are local records, but must never authorize arbitrary path deletion.
    if not doc['records'] or file.name != 'receipt.json' or file.parent.parent.name != '.ovizlab-backups':
        raise ValueError('Invalid rollback receipt location')
    for rec in doc['records']:
        dest = Path(rec.get('destination', ''))
        expected_root = file.parent.parent.parent
        if (not NAME_RE.fullmatch(rec.get('skill', '')) or dest.name != rec['skill']
                or dest.parent.name != 'skills' or dest.parent.parent != expected_root
                or not isinstance(rec.get('installed_files'), dict)
                or not all(SHA_RE.fullmatch(v) for v in rec['installed_files'].values())
                or (rec.get('backup') is not None and Path(rec['backup']) != file.parent / rec['skill'])):
            raise ValueError('Invalid rollback target or receipt')
    # Verify all targets before mutating any of them.
    for rec in doc['records']:
        dest = Path(rec['destination'])
        if current_digest(dest) != rec['installed_files']:
            raise ValueError('STOP: installed files modified since installation: ' + str(dest))
        if rec['backup'] and not Path(rec['backup']).is_dir():
            raise ValueError('STOP: backup missing: ' + rec['backup'])
    for rec in reversed(doc['records']):
        dest = Path(rec['destination'])
        shutil.rmtree(dest)
        if rec['backup']:
            Path(rec['backup']).rename(dest)
    # Keep receipt as evidence, mark used to prevent repeated destructive rollback.
    file.rename(file.with_suffix('.rolled-back.json'))
    return {'status': 'ROLLED_BACK', 'count': len(doc['records'])}


def main(argv=None):
    p = argparse.ArgumentParser(description='OVizLAB offline Agent Skills installer (dry-run by default)')
    p.add_argument('--bundle', type=Path, default=Path(__file__).resolve().parent)
    p.add_argument('--agent', choices=sorted(AGENTS), action='append')
    p.add_argument('--scope', choices=['user', 'project'], default='user')
    p.add_argument('--project-root', type=Path)
    p.add_argument('--skill', action='append')
    p.add_argument('--apply', action='store_true', help='Actually install after validation; otherwise dry-run only')
    p.add_argument('--rollback-receipt', type=Path)
    args = p.parse_args(argv)
    try:
        if args.rollback_receipt:
            if not args.apply:
                raise ValueError('Rollback requires --apply')
            result = rollback(args.rollback_receipt)
        else:
            if not args.agent:
                raise ValueError('Specify one or more --agent codex|claude|cursor|copilot')
            if args.apply:
                result = execute(args.bundle, args.agent, args.scope, args.project_root, selected=args.skill)
            else:
                info, _, plan = prepare_plan(args.bundle, args.agent, args.scope, args.project_root, selected=args.skill)
                result = {'status': 'DRY_RUN', 'source_commit': info['source_commit'], 'plan': plan}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        print('BLOCKED: ' + str(error), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
