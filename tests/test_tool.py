import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tool import capture, verify, parse_jevgrep, verify_batch

class ReceiptTests(unittest.TestCase):
    def test_exact_moved_stale(self):
        with tempfile.TemporaryDirectory() as tmp:
            file = Path(tmp) / 'a.py'
            file.write_text('one\ntwo\n')
            receipt = capture(tmp, 'a.py', 1, 2)
            self.assertEqual(verify(tmp, receipt)['status'], 'exact')
            file.write_text('zero\none\ntwo\n')
            self.assertEqual(verify(tmp, receipt)['status'], 'moved')
            file.write_text('zero\none\nthree\n')
            self.assertEqual(verify(tmp, receipt)['status'], 'stale')

    def test_escape_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                capture(tmp, '../outside.py', 1, 1)

    def test_jevgrep_receipt_detects_changed_source(self):
        root = Path(__file__).resolve().parents[1]
        output = (root / 'examples/jevgrep-output.txt').read_text()
        receipts = parse_jevgrep(root, output)
        self.assertEqual(len(receipts), 1)
        self.assertTrue(verify_batch(root, receipts)['ok'])
        with tempfile.TemporaryDirectory() as tmp:
            file = Path(tmp) / 'examples/source.py'
            file.parent.mkdir()
            file.write_text('def answer():\n    return 43\n')
            self.assertEqual(verify_batch(tmp, receipts)['results'][0]['status'], 'stale')

    def test_jevgrep_truncated_block_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                parse_jevgrep(tmp, 'Source block "a.py" lines 1-2:\n1: only one')
