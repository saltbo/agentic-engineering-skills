"""Exercise the path checker through its public CLI."""

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "skills/bep-best-openapi-design/scripts/check_resource_paths.py"
)


class ResourcePathTests(unittest.TestCase):
    def run_checker(self, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args], capture_output=True, text=True
        )

    def assert_exit(self, expected, *args):
        result = self.run_checker(*args)
        self.assertEqual(expected, result.returncode, result.stdout + result.stderr)

    def test_resource_paths_pass_bep(self):
        self.assert_exit(
            0, "--profile", "bep", "/orders", "/orders/{orderId}/cancellation-requests"
        )

    def test_file_mode_reads_paths_and_ignores_comments(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "paths.txt"
            path.write_text("# resources\n\n/orders\n/orders/{orderId}\n")
            self.assert_exit(0, "--file", str(path))

    def test_file_mode_rejects_an_invalid_member(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "paths.txt"
            path.write_text("/orders\n/orders/{orderId}/cancel\n")
            self.assert_exit(1, "--file", str(path))

    def test_empty_or_comment_only_file_cannot_report_success(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "paths.txt"
            for content in ("", "# no paths\n\n"):
                with self.subTest(content=content):
                    path.write_text(content)
                    self.assertNotEqual(0, self.run_checker("--file", str(path)).returncode)

    def test_bep_rejects_action_and_version_conventions(self):
        for path in (
            "/v1/orders",
            "/orders?api-version=2026-09-05",
            "/orders/{orderId}/cancel",
            "/orders/{orderId}:cancel",
            "/orders?action=cancel",
            "/orders/%63ancel",
            "/auditLogs",
        ):
            with self.subTest(path=path):
                self.assert_exit(1, "--profile", "bep", path)

    def test_existing_profile_preserves_legacy_contract_shapes(self):
        self.assert_exit(
            0, "--profile", "existing", "/v1/orders",
            "/orders?api-version=2026-09-05", "/orders/{order_id}:cancel", "/auditLogs",
        )

    def test_existing_profile_also_works_with_file_input(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "paths.txt"
            path.write_text("/v1/orders\n")
            self.assert_exit(0, "--profile", "existing", "--file", str(path))

    def test_bad_inputs_cannot_pass_either_profile(self):
        for profile in ("bep", "existing"):
            for path in ("orders", "https://example.com/orders", "/orders/{id", "/orders/{}"):
                with self.subTest(profile=profile, path=path):
                    self.assert_exit(1, "--profile", profile, path)

    def test_missing_or_conflicting_cli_input_fails(self):
        for args in ((), ("--profile", "unknown", "/orders"), ("--file", "paths.txt", "/orders")):
            with self.subTest(args=args):
                self.assert_exit(2, *args)


if __name__ == "__main__":
    unittest.main()
