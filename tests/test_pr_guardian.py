"""PR scanning must inspect UTF-8 diffs and reject failed Git commands."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCANNER = Path(__file__).resolve().parents[1] / "skills/pr-guardian/scripts/scan_diff.py"


class ScannerTests(unittest.TestCase):
    def scan(self, target):
        return subprocess.run(
            [sys.executable, str(SCANNER)], cwd=target, capture_output=True, text=True, encoding="utf-8", check=False
        )

    def test_unicode_diff_still_detects_breakpoint(self):
        with tempfile.TemporaryDirectory() as td:
            target = Path(td)

            def git(*args):
                subprocess.run(["git", *args], cwd=target, check=True, capture_output=True)

            git("init")
            source = target / "app.py"
            source.write_text("# initial\n", encoding="utf-8")
            git("add", "app.py")
            git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", "initial")
            source.write_text("# \u2014\nbreakpoint()\n", encoding="utf-8")
            result = self.scan(target)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("Python breakpoint", result.stderr)

    def test_git_error_is_not_clean(self):
        with tempfile.TemporaryDirectory() as td:
            result = self.scan(td)
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            self.assertNotIn("Clean:", result.stdout)


if __name__ == "__main__":
    unittest.main()
