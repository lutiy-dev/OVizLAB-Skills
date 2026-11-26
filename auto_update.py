"""Opt-in OVizLAB updater: pinned public channel, unchanged-owned-Skills only.

No scheduled task is created here. Run requires an explicit prior enrollment and
never executes code from the downloaded archive. Needs Python 3.10+ and local
agent_installer.py. No global settings or Codex hooks are changed.
"""
import argparse
from contextlib import contextmanager
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import tempfile
import urllib.request
import zipfile

from agent_installer import current_digest, execute, load_bundle

CHANNEL_URL = "https://raw.githubusercontent.com/lutiy-dev/OVizLAB-Skills/main/channel.json"
REPOSITORY = "lutiy-dev/OVizLAB-Skills"
MAX_CHANNEL_BYTES = 16384
MAX_ARCHIVE_BYTES = 16_000_000
MAX_EXPANDED_BYTES = 40_000_000
MAX_ENTRIES = 600
RELEASE_RE = re.compile(
    r"^https://github[.]com/lutiy-dev/OVizLAB-Skills/releases/download/"
    r"v[0-9]+[.][0-9]+[.][0-9]+/ovizlab-agent-installer[.]zip$")
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
SKILL_NAME = re.compile(r"^[a-z0-9][a-z0-9-]{1,79}$")


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def is_reparse(path):
    """Reject symlinks and Windows NTFS junction / reparse-point targets."""
    p = Path(path)
    if p.is_symlink():
        return True
    try:
        attrs = getattr(p.lstat(), "st_file_attributes", 0)
    except FileNotFoundError:
        return False
    return bool(attrs & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400))


def verify_physical_target(home, skills):
    root = Path(home)
    agent = root / ".agents"
    target = agent / "skills"
    for path in (root, agent, target):
        if is_reparse(path):
            raise ValueError("REPARSE_TARGET_BLOCKED")
    for name in skills:
        folder = target / name
        if is_reparse(folder):
            raise ValueError("REPARSE_SKILL_BLOCKED: " + name)
        if folder.is_dir():
            for child in folder.rglob("*"):
                if is_reparse(child):
                    raise ValueError("REPARSE_SKILL_CONTENT_BLOCKED: " + name)


def default_state_path():
    root = os.environ.get("LOCALAPPDATA")
    if not root:
        raise ValueError("LOCALAPPDATA_REQUIRED")
    return Path(root) / "OVizLAB" / "auto-update" / "state.json"


def download(url, limit):
    req = urllib.request.Request(url, headers={"User-Agent": "OVizLAB-Agent-Update/0.1"})
    with urllib.request.urlopen(req, timeout=25) as response:
        if response.status != 200:
            raise ValueError("HTTP_NOT_OK")
        effective = response.geturl()
        if not effective.startswith("https://"):
            raise ValueError("UNSAFE_REDIRECT")
        result = response.read(limit + 1)
    if len(result) > limit:
        raise ValueError("REMOTE_SIZE_LIMIT")
    return result


def channel(data):
    if not isinstance(data, dict):
        raise ValueError("INVALID_CHANNEL")
    if data.get("schema_version") != 1 or data.get("repository") != REPOSITORY:
        raise ValueError("CHANNEL_IDENTITY_MISMATCH")
    if type(data.get("sequence")) is not int or data["sequence"] < 1:
        raise ValueError("CHANNEL_SEQUENCE_INVALID")
    if not isinstance(data.get("source_commit"), str) or not HEX40.fullmatch(data["source_commit"]):
        raise ValueError("SOURCE_SHA_INVALID")
    if not isinstance(data.get("archive_sha256"), str) or not HEX64.fullmatch(data["archive_sha256"]):
        raise ValueError("ARCHIVE_SHA_INVALID")
    if not isinstance(data.get("archive_url"), str) or not RELEASE_RE.fullmatch(data["archive_url"]):
        raise ValueError("RELEASE_URL_UNTRUSTED")
    return data


def get_channel(fetch=download):
    payload = fetch(CHANNEL_URL, MAX_CHANNEL_BYTES)
    return channel(json.loads(payload.decode("utf-8")))


def read_state(path):
    path = Path(path)
    if path.is_symlink() or not path.is_file():
        raise ValueError("STATE_MISSING_OR_UNSAFE")
    s = json.loads(path.read_text(encoding="utf-8"))
    if (s.get("schema_version") != 1 or s.get("repository") != REPOSITORY
            or s.get("agent") != "codex" or type(s.get("sequence")) is not int
            or s["sequence"] < 1 or not HEX40.fullmatch(s.get("source_commit", ""))
            or not isinstance(s.get("home"), str)
            or not isinstance(s.get("installed"), dict) or not s["installed"]):
        raise ValueError("INVALID_STATE")
    home = Path(s["home"])
    if not home.is_absolute() or home.is_symlink() or not home.is_dir():
        raise ValueError("HOME_UNAVAILABLE")
    for name, hashes in s["installed"].items():
        if not SKILL_NAME.fullmatch(name) or not isinstance(hashes, dict) or not hashes:
            raise ValueError("INVALID_SKILL_STATE")
        if not all(isinstance(p, str) and p and ".." not in PurePosixPath(p).parts
                   and isinstance(d, str) and HEX64.fullmatch(d) for p, d in hashes.items()):
            raise ValueError("INVALID_FILE_STATE")
    return s


def save_state(path, data, must_not_exist=False):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.is_symlink() or (must_not_exist and path.exists()):
        raise ValueError("STATE_ALREADY_EXISTS_OR_SYMLINK")
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent,
                                     prefix=".ovizlab-", suffix=".tmp",
                                     delete=False) as handle:
        temp = Path(handle.name)
        os.chmod(temp, 0o600)
        json.dump(data, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    try:
        os.replace(temp, path)
    finally:
        if temp.exists():
            temp.unlink()


@contextmanager
def lock_state(path):
    p = Path(str(path) + ".lock")
    p.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(p, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    try:
        os.close(fd)
        yield
    finally:
        p.unlink(missing_ok=True)


def installed_hashes(bundle, home):
    info, data = load_bundle(bundle)
    home = Path(home).absolute()
    root = home / ".agents" / "skills"
    verify_physical_target(home, info["skills"])
    if root.is_symlink() or not root.is_dir():
        raise ValueError("TARGET_SKILLS_MISSING")
    expected = {}
    for skill in info["skills"]:
        dest = root / skill
        if not dest.is_dir() or dest.is_symlink():
            raise ValueError("NOT_INSTALLED: " + skill)
        wanted = {p.split("/", 2)[2]: sha256(raw)
                  for p, raw in data.items() if p.startswith("skills/" + skill + "/")}
        if current_digest(dest) != wanted:
            raise ValueError("LOCAL_DRIFT_OR_OLD_VERSION: " + skill)
        expected[skill] = wanted
    return info, expected


def enroll(state_path, bundle, home, sequence):
    if type(sequence) is not int or sequence < 1:
        raise ValueError("SEQUENCE_REQUIRED")
    state_path = Path(state_path)
    with lock_state(state_path):
        if state_path.exists():
            raise ValueError("ENROLLED_ALREADY")
        info, installed = installed_hashes(bundle, home)
        value = {"schema_version": 1, "repository": REPOSITORY, "agent": "codex",
                 "home": str(Path(home).absolute()), "sequence": sequence,
                 "source_commit": info["source_commit"], "installed": installed,
                 "last_receipts": []}
        save_state(state_path, value, must_not_exist=True)
    return {"status": "ENROLLED", "skills": len(installed), "source_commit": info["source_commit"],
            "background_task_installed": False}


def verify_owned(s):
    root = Path(s["home"]) / ".agents" / "skills"
    verify_physical_target(s["home"], s["installed"])
    if root.is_symlink() or not root.is_dir():
        raise ValueError("TARGET_SKILLS_MISSING")
    for name, hashes in s["installed"].items():
        path = root / name
        if not path.is_dir() or path.is_symlink() or current_digest(path) != hashes:
            raise ValueError("LOCAL_CHANGES_BLOCK_UPDATE: " + name)


def unpack_bundle(blob, directory):
    target = Path(directory)
    with zipfile.ZipFile(io.BytesIO(blob)) as archive:
        members = archive.infolist()
        if not members or len(members) > MAX_ENTRIES:
            raise ValueError("ARCHIVE_MEMBER_COUNT")
        total = 0
        names = set()
        for item in members:
            name = item.filename
            parts = PurePosixPath(name).parts
            mode = (item.external_attr >> 16) & 0xFFFF
            if (not name or name.startswith("/") or "\\" in name
                    or ":" in name or any(p in (".", "..") for p in parts)
                    or len(parts) < 1 or not all(p and not p.endswith((" ", ".")) for p in parts)
                    or stat.S_ISLNK(mode) or (mode and not (stat.S_ISREG(mode) or stat.S_ISDIR(mode)))):
                raise ValueError("UNSAFE_ZIP_MEMBER")
            key = name.casefold().rstrip("/")
            if key in names:
                raise ValueError("ZIP_CASE_COLLISION")
            names.add(key)
            total += item.file_size
            if total > MAX_EXPANDED_BYTES:
                raise ValueError("ZIP_EXPANSION_LIMIT")
        for item in members:
            dest = target.joinpath(*PurePosixPath(item.filename).parts)
            if item.is_dir():
                dest.mkdir(parents=True, exist_ok=True)
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            with archive.open(item) as source, dest.open("wb") as out:
                while True:
                    chunk = source.read(1024 * 1024)
                    if not chunk:
                        break
                    out.write(chunk)


def run_once(state_path, fetch=download, check_only=False):
    state_path = Path(state_path)
    with lock_state(state_path):
        s = read_state(state_path)
        latest = get_channel(fetch)
        if latest["sequence"] < s["sequence"]:
            raise ValueError("CHANNEL_ROLLBACK_BLOCKED")
        if latest["sequence"] == s["sequence"]:
            if latest["source_commit"] != s["source_commit"]:
                raise ValueError("SAME_VERSION_CHANGED")
            return {"status": "UP_TO_DATE", "sequence": s["sequence"]}
        if latest["source_commit"] == s["source_commit"]:
            raise ValueError("SEQUENCE_WITHOUT_NEW_COMMIT")
        if check_only:
            return {"status": "UPDATE_AVAILABLE", "sequence": latest["sequence"],
                    "source_commit": latest["source_commit"], "write_performed": False}
        verify_owned(s)
        payload = fetch(latest["archive_url"], MAX_ARCHIVE_BYTES)
        if sha256(payload) != latest["archive_sha256"]:
            raise ValueError("ARCHIVE_CHECKSUM_MISMATCH")
        with tempfile.TemporaryDirectory(prefix="ovizlab-update-") as temp:
            bundle = Path(temp)
            unpack_bundle(payload, bundle)
            info, content = load_bundle(bundle)
            if info["source_commit"] != latest["source_commit"]:
                raise ValueError("SOURCE_COMMIT_MISMATCH")
            if not set(s["installed"]).issubset(set(info["skills"])):
                raise ValueError("OWNED_SKILL_REMOVED")
            # Refuse unrelated new skills: additions require independent approval.
            selected = sorted(s["installed"])
            expected = {name: {p.split("/", 2)[2]: sha256(raw)
                               for p, raw in content.items() if p.startswith("skills/" + name + "/")}
                        for name in selected}
            result = execute(bundle, ["codex"], "user", home=Path(s["home"]), selected=selected)
            s["installed"] = expected
            s["sequence"] = latest["sequence"]
            s["source_commit"] = info["source_commit"]
            s["last_receipts"] = result["receipts"]
            save_state(state_path, s)
        return {"status": "UPDATED", "sequence": s["sequence"], "skills": len(selected),
                "receipts": s["last_receipts"],
                "new_skills_skipped": sorted(set(info["skills"]) - set(selected)),
                "codex_runtime_loading": "NOT TESTED"}


def main(argv=None):
    cli = argparse.ArgumentParser(description="OVizLAB opt-in background Skills updater")
    cli.add_argument("command", choices=["enroll", "run", "check", "status"])
    cli.add_argument("--state", type=Path)
    cli.add_argument("--bundle", type=Path)
    cli.add_argument("--home", type=Path)
    cli.add_argument("--sequence", type=int)
    args = cli.parse_args(argv)
    try:
        state = args.state or default_state_path()
        if args.command == "enroll":
            if not args.bundle or not args.home or args.sequence is None:
                raise ValueError("ENROLL_REQUIRES_BUNDLE_HOME_SEQUENCE")
            out = enroll(state, args.bundle, args.home, args.sequence)
        elif args.command == "status":
            s = read_state(state)
            out = {"status": "ENROLLED", "sequence": s["sequence"],
                   "source_commit": s["source_commit"], "skills": len(s["installed"])}
        else:
            out = run_once(state, check_only=args.command == "check")
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, KeyError, json.JSONDecodeError,
            zipfile.BadZipFile, UnicodeError) as error:
        print(json.dumps({"status": "BLOCKED", "reason": str(error)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
