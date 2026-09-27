import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tool import capture, verify

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
