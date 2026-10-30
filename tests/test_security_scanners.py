import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from scripts import check_dependency_lock, check_no_signer, check_secrets


class SecurityScannerTests(unittest.TestCase):
    def test_secret_pattern_is_detected(self) -> None:
        content = b"api" + b"_key = '" + b"placeholder-" + b"example'"
        self.assertTrue(check_secrets.contains_secret(content))

    def test_ordinary_configuration_is_not_a_secret(self) -> None:
        self.assertFalse(check_secrets.contains_secret(b"timeout = 30\n"))

    def test_signing_and_sending_apis_are_detected(self) -> None:
        source = "Key" + "pair()" + "\nclient." + "send" + "Transaction()"
        self.assertTrue(check_no_signer.contains_forbidden_code(source))

    def test_simulation_only_code_is_allowed(self) -> None:
        source = "class SimulatedFill:\n    fee_lamports = 0\n"
        self.assertFalse(check_no_signer.contains_forbidden_code(source))

    def test_dependency_lock_requires_exact_pins_and_hashes(self) -> None:
        with TemporaryDirectory() as directory:
            direct_path = Path(directory) / "requirements.in"
            lock_path = Path(directory) / "requirements.lock"
            direct_path.write_text("ruff==0.16.0\n", encoding="utf-8")
            lock_path.write_text(
                "ruff==0.16.0 --hash=sha256:" + ("a" * 64) + "\n",
                encoding="utf-8",
            )
            direct = check_dependency_lock._read_pins(direct_path, require_hashes=False)
            locked = check_dependency_lock._read_pins(lock_path, require_hashes=True)
        self.assertEqual(direct["ruff"][0], locked["ruff"][0])
        self.assertEqual(len(locked["ruff"][1] or ""), 64)


if __name__ == "__main__":
    unittest.main()
