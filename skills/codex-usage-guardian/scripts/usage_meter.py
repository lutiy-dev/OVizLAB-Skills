"""Local Codex usage snapshots. Standard library only; no network or prompt export."""
import argparse
import hashlib
import json
import os
import re
import sys
import time
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

KEYS = ('input_tokens', 'cached_input_tokens', 'output_tokens',
        'reasoning_output_tokens', 'total_tokens')
SID = re.compile(r'^[a-zA-Z0-9_-]{1,100}$')


def counts(value):
    if not isinstance(value, dict):
        return None
    result = {k: value[k] for k in KEYS if isinstance(value.get(k), int)
              and not isinstance(value[k], bool) and value[k] >= 0}
    return result if 'total_tokens' in result else None


def difference(current, previous):
    if not current or not previous:
        return None
    result = {k: current[k] - previous[k] for k in current.keys() & previous.keys()}
    return result if all(v >= 0 for v in result.values()) else None


def limits(value):
    if not isinstance(value, dict):
        return None
    result = {k: value.get(k) for k in ('limit_id', 'plan_type')}
    for key in ('primary', 'secondary'):
        w = value.get(key)
        if isinstance(w, dict) and isinstance(w.get('used_percent'), (int, float)):
            result[key] = {k: w.get(k) for k in ('used_percent', 'window_minutes', 'resets_at')}
    return result if any(k in result for k in ('primary', 'secondary')) else None


def limit_change(current, previous):
    result = {}
    if not current or not previous:
        return result
    if any(current.get(k) != previous.get(k) for k in ('limit_id', 'plan_type')):
        return result
    for key in ('primary', 'secondary'):
        a, b = current.get(key), previous.get(key)
        if a and b and a.get('resets_at') is not None and all(
                a.get(k) == b.get(k) for k in ('window_minutes', 'resets_at')):
            delta = a['used_percent'] - b['used_percent']
            if delta >= 0:
                result[key] = round(delta, 6)
    return result


def consume(state, row):
    kind, p = row.get('type'), row.get('payload')
    if not isinstance(p, dict):
        return
    stamp = row.get('timestamp')
    if kind == 'turn_context':
        if p.get('turn_id') != state.get('turn_id'):
            state['turn_baseline'] = state.get('total')
            state['turn'] = None
            state['turn_id'] = p.get('turn_id')
        state['model'] = p.get('model', state.get('model'))
    elif kind == 'token_usage_record':
        total = counts(p.get('thread_token_usage'))
        if total:
            state.update(total=total, turn=counts(p.get('turn_token_usage')),
                         last_request=counts(p.get('usage')), turn_id=p.get('turn_id'),
                         usage_timestamp=stamp, modern=True, source='token_usage_record')
    elif kind == 'event_msg' and p.get('type') == 'token_count':
        quota = limits(p.get('rate_limits'))
        if quota:
            state.update(rate_limits=quota, limits_timestamp=stamp)
        info = p.get('info') or {}
        total = counts(info.get('total_token_usage'))
        if total and not state.get('modern'):
            state.update(total=total, last_request=counts(info.get('last_token_usage')),
                         usage_timestamp=stamp, source='token_count')
            state['turn'] = difference(total, state.get('turn_baseline'))


def scan(path, state):
    """Incremental binary scan; never consume an unfinished trailing JSON line."""
    stat = path.stat()
    with path.open('rb') as stream:
        fingerprint = hashlib.sha256(stream.read(128)).hexdigest()
        identity = [stat.st_dev, stat.st_ino, fingerprint]
        if state.get('identity') != identity or stat.st_size < state.get('offset', 0):
            state = {'identity': identity, 'offset': 0}
        stream.seek(state.get('offset', 0))
        while True:
            start = stream.tell()
            line = stream.readline()
            if not line:
                break
            if not line.endswith(b'\n'):
                state['offset'] = start
                break
            state['offset'] = stream.tell()
            try:
                row = json.loads(line)
                if isinstance(row, dict):
                    consume(state, row)
            except (ValueError, UnicodeError):
                state['malformed_lines'] = state.get('malformed_lines', 0) + 1
    return state


def report(state, previous=None):
    total = state.get('total')
    return {
        'status': 'OBSERVED' if total else 'NOT CONFIRMED',
        'observed_at': datetime.now(timezone.utc).isoformat(),
        'model': state.get('model'), 'turn_id': state.get('turn_id'),
        'source': state.get('source'), 'usage_timestamp': state.get('usage_timestamp'),
        'limits_timestamp': state.get('limits_timestamp'),
        'session_tokens': total, 'turn_tokens': state.get('turn'),
        'last_request_tokens': state.get('last_request'),
        'since_previous_snapshot': difference(total, (previous or {}).get('session_tokens')),
        'rate_limits': state.get('rate_limits'),
        'account_limit_change_pp': limit_change(state.get('rate_limits'), (previous or {}).get('rate_limits')),
        'malformed_lines': state.get('malformed_lines', 0),
        'savings': 'NOT CONFIRMED: requires a comparable baseline',
        'attribution': 'Account limits may include other chats. Snapshot is not per-tool billing.',
        'coverage': 'This transcript only; other threads and agents are not aggregated.',
    }


def short(r):
    def number(v):
        return f'{v:,}'.replace(',', ' ') if v is not None else '?'
    total = r.get('session_tokens') or {}
    turn = r.get('turn_tokens') or {}
    delta = r.get('since_previous_snapshot') or {}
    q = r.get('rate_limits') or {}
    windows = []
    for k in ('primary', 'secondary'):
        w = q.get(k)
        if w:
            windows.append(f"{w.get('window_minutes', '?')} мин: {w['used_percent']:g}% использовано")
    return (f"Расход: +{number(delta.get('total_tokens'))} ток. с прошлого замера; "
            f"ход {number(turn.get('total_tokens'))}; чат {number(total.get('total_tokens'))} "
            f"(кэш {number(total.get('cached_input_tokens'))} внутри входных). "
            + ('; '.join(windows) or 'Лимиты: нет данных')
            + f". Замер токенов {r.get('usage_timestamp') or '?'}; лимитов {r.get('limits_timestamp') or '?'}. "
            'Не стоимость отдельного инструмента; экономия не измерена.')


@contextmanager
def lock(path):
    deadline = time.monotonic() + 2
    while True:
        try:
            fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
            break
        except FileExistsError:
            # Fail open on contention; never remove another process's lock.
            if time.monotonic() >= deadline:
                raise RuntimeError('meter busy; no new snapshot')
            time.sleep(0.025)
    try:
        os.close(fd)
        yield
    finally:
        path.unlink(missing_ok=True)


def write_json(path, value):
    temp = path.with_suffix(path.suffix + f'.{os.getpid()}.tmp')
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    os.replace(temp, path)


def find_transcript(home, session):
    if not session or not SID.fullmatch(session):
        raise ValueError('Specify --session or CODEX_THREAD_ID; no latest-chat guessing')
    matches = list((home / 'sessions').glob(f'*/*/*/*{session}.jsonl'))
    if len(matches) != 1:
        raise ValueError(f'Expected one transcript, found {len(matches)}')
    return matches[0]


def sample(path, output, session, event='manual', tool=None):
    if not SID.fullmatch(session):
        raise ValueError('Invalid session id')
    output.mkdir(parents=True, exist_ok=True)
    with lock(output / f'{session}.lock'):
        state_path = output / f'{session}.state.json'
        latest_path = output / f'{session}.latest.json'
        state = json.loads(state_path.read_text(encoding='utf-8')) if state_path.exists() else {}
        previous = json.loads(latest_path.read_text(encoding='utf-8')) if latest_path.exists() else None
        state = scan(path, state)
        r = report(state, previous)
        r.update(session_id=session, hook_event=event)
        # No tool arguments, outputs, prompts, cwd, credentials or message bodies stored.
        if tool:
            r['tool'] = re.sub(r'[^a-zA-Z0-9_.:-]', '_', tool)[:80]
        write_json(state_path, state)
        write_json(latest_path, r)
        with (output / f'{session}.events.jsonl').open('a', encoding='utf-8') as f:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')
        (output / f'{session}.latest.txt').write_text(short(r) + '\n', encoding='utf-8')
        return r


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--home', type=Path, default=Path(os.environ.get('CODEX_HOME', str(Path.home() / '.codex'))))
    ap.add_argument('--output', type=Path)
    ap.add_argument('--session', default=os.environ.get('CODEX_THREAD_ID'))
    ap.add_argument('--file', type=Path, help='Explicit transcript for manual/offline use')
    ap.add_argument('--hook', action='store_true', help='Read a Codex hook payload from stdin')
    ap.add_argument('--json', action='store_true')
    args = ap.parse_args(argv)
    try:
        home = args.home.resolve()
        payload = json.load(sys.stdin) if args.hook else {}
        session = payload.get('session_id') or args.session
        event = payload.get('hook_event_name', 'manual')
        if args.hook:
            path_value = payload.get('transcript_path')
            path = Path(path_value).resolve() if path_value else find_transcript(home, session)
            if not path.is_relative_to((home / 'sessions').resolve()):
                raise ValueError('Hook transcript must be inside CODEX_HOME/sessions')
            if not path.name.endswith(f'{session}.jsonl'):
                raise ValueError('Transcript/session mismatch')
        else:
            path = args.file.resolve() if args.file else find_transcript(home, session)
        r = sample(path, args.output or home / 'usage-guardian', session, event, payload.get('tool_name'))
        if args.hook:
            print(json.dumps({'systemMessage': short(r)}, ensure_ascii=False))
        else:
            print(json.dumps(r, ensure_ascii=False, indent=2) if args.json else short(r))
        return 0
    except (OSError, ValueError, RuntimeError, TypeError) as exc:
        # Hooks never block or continue a model turn. No stack/message content export.
        message = 'Usage meter unavailable: ' + type(exc).__name__
        print(json.dumps({'systemMessage': message}) if args.hook else message)
        return 0 if args.hook else 1


if __name__ == '__main__':
    sys.exit(main())
