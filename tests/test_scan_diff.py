"""Tests for skills/pr-guardian/scripts/scan_diff.py (stdlib unittest)."""

import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "skills/pr-guardian/scripts/scan_diff.py"
_spec = importlib.util.spec_from_file_location("scan_diff", SCRIPT)
scan_diff = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(scan_diff)

SECRET = "ghp_" + "a" * 36


def make_diff(path: str, *added: str) -> str:
    lines = [f"diff --git a/{path} b/{path}", f"--- a/{path}", f"+++ b/{path}", "@@ -1 +1,2 @@", " x"]
    return "\n".join(lines + [f"+{line}" for line in added]) + "\n"


class ScanAllowPrintTest(unittest.TestCase):
    def test_print_in_allowed_file_is_not_reported(self):  # AC1
        diff = make_diff("scripts/foo.py", 'print("PASS")')
        self.assertEqual(scan_diff.scan(diff, allow_print=["scripts/*"]), [])

    def test_print_reported_without_allowlist(self):  # AC2
        warnings = scan_diff.scan(make_diff("scripts/foo.py", 'print("PASS")'))
        self.assertEqual(len(warnings), 1)
        self.assertIn("DEBUG CODE in scripts/foo.py", warnings[0])

    def test_print_in_other_file_still_reported(self):  # AC2
        diff = make_diff("app/main.py", 'print("debug")')
        self.assertEqual(len(scan_diff.scan(diff, allow_print=["scripts/*"])), 1)

    def test_secret_in_allowed_file_still_reported(self):  # AC3
        diff = make_diff("scripts/foo.py", f'TOKEN = "{SECRET}"')
        warnings = scan_diff.scan(diff, allow_print=["scripts/*"])
        self.assertEqual(len(warnings), 1)
        self.assertIn("POSSIBLE SECRET", warnings[0])

    def test_breakpoint_in_allowed_file_still_reported(self):  # AC4
        warnings = scan_diff.scan(make_diff("scripts/foo.py", "breakpoint()"), allow_print=["scripts/*"])
        self.assertEqual(len(warnings), 1)
        self.assertIn("breakpoint", warnings[0])

    def test_cli_accepts_repeated_allow_print(self):  # AC5
        args = scan_diff.parse_args(["--allow-print", "scripts/*", "--allow-print", "skills/*/scripts/*"])
        self.assertEqual(args.allow_print, ["scripts/*", "skills/*/scripts/*"])

    def test_cli_defaults_to_no_allowlist(self):  # AC5
        self.assertEqual(scan_diff.parse_args([]).allow_print, [])


if __name__ == "__main__":
    unittest.main()
