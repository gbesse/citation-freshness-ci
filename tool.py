"""Local source-span receipts and freshness verification."""
import hashlib
import json
import re
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


def parse_jevgrep(root, output):
    """Parse Jevgrep's documented numbered Source block stdout format."""
    lines = output.splitlines()
    receipts = []
    header = re.compile(r'^Source block "(.+)" lines (\d+)-(\d+):$')
    numbered = re.compile(r'^(\d+): ?(.*)$')
    index = 0
    while index < len(lines):
        match = header.match(lines[index])
        if not match:
            index += 1
            continue
        path, start, end = match.group(1), int(match.group(2)), int(match.group(3))
        resolve(root, path)
        if start < 1 or end < start:
            raise ValueError(f'invalid Jevgrep span: {path}')
        excerpt = []
        index += 1
        for number in range(start, end + 1):
            if index >= len(lines):
                raise ValueError(f'incomplete Jevgrep source block: {path}')
            line = numbered.match(lines[index])
            if not line or int(line.group(1)) != number:
                raise ValueError(f'non-contiguous Jevgrep source block: {path}')
            excerpt.append(line.group(2))
            index += 1
        receipts.append({'path': path, 'start': start, 'end': end, 'excerpt': excerpt,
                         'sha256': hashlib.sha256('\n'.join(excerpt).encode()).hexdigest()})
    if not receipts:
        raise ValueError('no Jevgrep Source block found')
    return receipts


def verify_batch(root, receipts):
    results = [{'path': receipt['path'], **verify(root, receipt)} for receipt in receipts]
    return {'ok': all(item['ok'] for item in results), 'results': results}


def main():
    if len(sys.argv) < 2:
        raise SystemExit('usage: tool.py demo | capture PATH START END | verify ROOT RECEIPT.json | capture-jevgrep ROOT OUTPUT.txt | verify-batch ROOT RECEIPTS.json')
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
    if command == 'capture-jevgrep':
        receipts = parse_jevgrep(sys.argv[2], Path(sys.argv[3]).read_text())
        print(json.dumps(receipts, indent=2))
        return 0
    if command == 'verify-batch':
        result = verify_batch(sys.argv[2], json.loads(Path(sys.argv[3]).read_text()))
        print(json.dumps(result, indent=2))
        return 0 if result['ok'] else 1
    raise SystemExit('unknown command')

if __name__ == '__main__':
    raise SystemExit(main())
