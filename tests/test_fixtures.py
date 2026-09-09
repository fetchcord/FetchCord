"""Golden-fixture tests for hardware detection.

Each fixture is a real or representative `fastfetch --format json` capture
from a different machine type. They let the parser/mapping logic be exercised
deterministically in CI across platforms we don't actually have runners for.

- fastfetch_debian.json  : real capture from a Debian 13 container (includes
                           errored GPU and Font modules).
- fastfetch_macos.json   : representative Apple Silicon (macOS 15.1) machine.
- fastfetch_windows.json : representative Windows 11 + NVIDIA GPU machine.
"""

import unittest
from pathlib import Path

from fetch_cord.info import parse_fastfetch_json

FIXTURES = Path(__file__).parent / "fixtures"


class TestFastfetchFixtures(unittest.TestCase):
    @staticmethod
    def _fixtures() -> list[Path]:
        return sorted(FIXTURES.glob("fastfetch_*.json"))

    def _parse(self, name: str) -> dict[str, str]:
        return parse_fastfetch_json((FIXTURES / name).read_text())

    def test_debian_real_capture(self) -> None:
        fields = self._parse("fastfetch_debian.json")
        self.assertEqual(fields["os"], "Debian GNU/Linux 13.4 (trixie)")
        self.assertEqual(fields["kernel"], "6.12.91-fly")
        self.assertEqual(fields["cpu"], "AMD EPYC")
        self.assertEqual(fields["packages"], "432")
        self.assertEqual(fields["shell"], "bash")
        # GPU and Font errored in the real capture -> gracefully skipped.
        self.assertNotIn("gpu", fields)
        self.assertNotIn("font", fields)

    def test_macos_representative(self) -> None:
        fields = self._parse("fastfetch_macos.json")
        self.assertEqual(fields["os"], "macOS 15.1")
        self.assertEqual(fields["kernel"], "24.3.0")
        self.assertEqual(fields["cpu"], "Apple M4 Pro")
        self.assertEqual(fields["gpu"], "Apple M4 Pro")
        self.assertEqual(fields["shell"], "zsh")

    def test_windows_representative(self) -> None:
        fields = self._parse("fastfetch_windows.json")
        self.assertEqual(fields["os"], "Windows 11 Pro")
        self.assertEqual(fields["kernel"], "10.0.22631")
        self.assertEqual(fields["cpu"], "AMD Ryzen 7 7800X3D")
        self.assertEqual(fields["gpu"], "NVIDIA GeForce RTX 4080")

    def test_memory_formatted_gb(self) -> None:
        fields = self._parse("fastfetch_windows.json")
        self.assertRegex(fields["memory"], r"^\d+\.\d{2} GB / \d+\.\d{2} GB$")

    def test_every_fixture_has_os_and_kernel(self) -> None:
        for fixture in self._fixtures():
            with self.subTest(fixture=fixture.name):
                fields = parse_fastfetch_json(fixture.read_text())
                self.assertIn("os", fields, fixture.name)
                self.assertIn("kernel", fields, fixture.name)

    def test_every_fixture_parses_as_list_of_dicts(self) -> None:
        # Guard against a fixture accidentally holding invalid JSON.
        for fixture in self._fixtures():
            with self.subTest(fixture=fixture.name):
                self.assertIsInstance(parse_fastfetch_json(fixture.read_text()), dict)


if __name__ == "__main__":
    unittest.main(verbosity=2)
