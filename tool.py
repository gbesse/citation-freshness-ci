"""Local source-span receipts and freshness verification."""
import hashlib
import json
import sys
import tempfile
from pathlib import Path


def resolve(root, relative):
    root = Path(root).resolve()
    target = (root / relative).resolve()
    if target != root and root not in target.parents:
        raise ValueError('path escapes root')
    return target


def capture(root, relative, start, end):
    target = resolve(root, relative)
    lines = target.read_text().splitlines()
    if start < 1 or end < start or end > len(lines):
        raise ValueError('invalid line span')
    excerpt = lines[start - 1:end]
    return {'path': relative, 'start': start, 'end': end, 'excerpt': excerpt,
            'sha256': hashlib.sha256('\n'.join(excerpt).encode()).hexdigest()}


def verify(root, receipt):
    target = resolve(root, receipt['path'])
    if not target.exists():
        return {'status': 'missing', 'ok': False}
    lines = target.read_text().splitlines()
    excerpt = receipt['excerpt']
    if hashlib.sha256('\n'.join(excerpt).encode()).hexdigest() != receipt['sha256']:
        return {'status': 'invalid_receipt', 'ok': False}
    start, end = receipt['start'], receipt['end']
    if lines[start - 1:end] == excerpt:
        return {'status': 'exact', 'ok': True, 'start': start}
    locations = [i + 1 for i in range(len(lines) - len(excerpt) + 1) if lines[i:i + len(excerpt)] == excerpt]
    if len(locations) == 1:
        return {'status': 'moved', 'ok': True, 'start': locations[0]}
    if locations:
        return {'status': 'ambiguous', 'ok': False, 'locations': locations}
    return {'status': 'stale', 'ok': False}


def main():
    if len(sys.argv) < 2:
        raise SystemExit('usage: tool.py demo | capture PATH START END | verify ROOT RECEIPT.json')
    command = sys.argv[1]
    if command == 'demo':
        with tempfile.TemporaryDirectory() as tmp:
            file = Path(tmp) / 'source.py'
            file.write_text('def answer():\n    return 42\n')
            receipt = capture(tmp, 'source.py', 1, 2)
            exact = verify(tmp, receipt)
            file.write_text('# comment\ndef answer():\n    return 42\n')
            moved = verify(tmp, receipt)
            file.write_text('# comment\ndef answer():\n    return 43\n')
            stale = verify(tmp, receipt)
        print(json.dumps({'exact': exact, 'moved': moved, 'stale': stale}, indent=2))
        return 0 if exact['ok'] and moved['ok'] and not stale['ok'] else 1
    if command == 'capture':
        relative = sys.argv[2]
        print(json.dumps(capture(Path.cwd(), relative, int(sys.argv[3]), int(sys.argv[4])), indent=2))
        return 0
    if command == 'verify':
        result = verify(sys.argv[2], json.loads(Path(sys.argv[3]).read_text()))
        print(json.dumps(result, indent=2))
        return 0 if result['ok'] else 1
    raise SystemExit('unknown command')

if __name__ == '__main__':
    raise SystemExit(main())
