"""A duplicated excerpt is ambiguous even when its bytes still match."""
import json
import tempfile
from pathlib import Path

from tool import capture, verify

with tempfile.TemporaryDirectory() as folder:
    source = Path(folder) / "source.py"
    source.write_text("def answer():\n    return 42\n")
    receipt = capture(folder, "source.py", 1, 2)
    source.write_text("# copy A\ndef answer():\n    return 42\n# copy B\ndef answer():\n    return 42\n")
    result = verify(folder, receipt)
assert result["status"] == "ambiguous" and not result["ok"]
print(json.dumps({"source": "synthetic temporary file", "status": result["status"], "locations": result["locations"]}, sort_keys=True))
