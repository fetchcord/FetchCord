"""Tests for the native Windows fetchers and the NativeProvider wiring.

The registry is faked at the fetcher boundary so these run on any OS, which
keeps them useful on the Linux CI runner.
"""

import subprocess
import unittest
from collections.abc import Iterator
from contextlib import contextmanager
from unittest.mock import MagicMock, patch

from fetch_cord.fetch import NativeProvider

CURRENT_VERSION = "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion"
BIOS = "HARDWARE\\DESCRIPTION\\System\\BIOS"
CPU0 = "HARDWARE\\DESCRIPTION\\System\\CentralProcessor\\0"

# Values as the registry actually reports them on a Windows 11 machine. Note
# ProductName still says "Windows 10" - the build number is what distinguishes
# the release.
REGISTRY = {
    (CURRENT_VERSION, "ProductName"): "Windows 10 Pro",
    (CURRENT_VERSION, "CurrentBuildNumber"): "26100",
    (CURRENT_VERSION, "CurrentMajorVersionNumber"): "10",
    (CURRENT_VERSION, "CurrentMinorVersionNumber"): "0",
    (CPU0, "ProcessorNameString"): "Intel(R) Core(TM) i7-9750H CPU @ 2.60GHz",
    (BIOS, "BaseBoardManufacturer"): "ASUSTeK COMPUTER INC.",
    (BIOS, "BaseBoardProduct"): "PRIME B760-PLUS D4",
}


@contextmanager
def fake_registry(
    values: dict[tuple[str, str], str] | None = None,
) -> Iterator[MagicMock]:
    """Patch the registry helper with a fixed set of values."""
    table = REGISTRY if values is None else values

    def read(path: str, name: str) -> str | None:
        return table.get((path, name))

    with patch(
        "fetch_cord.native.Windows.registry.read", side_effect=read
    ) as mock_read:
        yield mock_read


class TestWindowsFetchers(unittest.TestCase):
    """Each fetcher must return the same shape the PowerShell command did."""

    def test_os_corrects_the_stale_product_name(self) -> None:
        from fetch_cord.native.Windows import os_info

        with fake_registry():
            self.assertEqual(os_info.fetch(), "Microsoft Windows 11 Pro")

    def test_os_leaves_windows_10_alone(self) -> None:
        from fetch_cord.native.Windows import os_info

        values = dict(REGISTRY)
        values[(CURRENT_VERSION, "CurrentBuildNumber")] = "19045"

        with fake_registry(values):
            self.assertEqual(os_info.fetch(), "Microsoft Windows 10 Pro")

    def test_kernel_matches_win32_version(self) -> None:
        from fetch_cord.native.Windows import kernel

        with fake_registry():
            self.assertEqual(kernel.fetch(), "10.0.26100")

    def test_cpu_matches_win32_name(self) -> None:
        from fetch_cord.native.Windows import cpu

        with fake_registry():
            self.assertEqual(cpu.fetch(), "Intel(R) Core(TM) i7-9750H CPU @ 2.60GHz")

    def test_motherboard_and_host(self) -> None:
        from fetch_cord.native.Windows import host, motherboard

        with fake_registry():
            self.assertEqual(motherboard.fetch(), "ASUSTeK COMPUTER INC.")
            self.assertEqual(host.fetch(), "PRIME B760-PLUS D4")

    def test_oem_placeholders_are_not_reported(self) -> None:
        """Firmware boilerplate should let another provider supply the value."""
        from fetch_cord.native.Windows import motherboard

        values = dict(REGISTRY)
        values[(BIOS, "BaseBoardManufacturer")] = "To Be Filled By O.E.M."

        with fake_registry(values):
            self.assertIsNone(motherboard.fetch())

    def test_unreadable_registry_returns_none(self) -> None:
        from fetch_cord.native.Windows import cpu, kernel, os_info

        with fake_registry({}):
            self.assertIsNone(os_info.fetch())
            self.assertIsNone(kernel.fetch())
            self.assertIsNone(cpu.fetch())

    def test_mem_matches_the_command_format(self) -> None:
        from fetch_cord.native.Windows import mem

        memory = MagicMock(total=32 * 1024**3, available=20 * 1024**3)
        with patch(
            "fetch_cord.native.Windows.mem.psutil.virtual_memory", return_value=memory
        ):
            self.assertEqual(mem.fetch(), "12.00 GB / 32.00 GB")


class TestNativeProvider(unittest.TestCase):
    def test_returns_the_fields_it_can_read(self) -> None:
        with patch(
            "fetch_cord.fetch.native_module.fetch",
            side_effect=lambda component: {
                "cpu": "AMD",
                "os": "Microsoft Windows 11 Pro",
            }.get(component),
        ):
            fields = NativeProvider().fetch()

        self.assertEqual(fields, {"cpu": "AMD", "os": "Microsoft Windows 11 Pro"})

    def test_skips_fields_an_earlier_provider_supplied(self) -> None:
        """Gap-filling is how Fetch.snapshot composes providers."""
        calls = []

        def record(component: str) -> str:
            calls.append(component)
            return "value"

        with patch("fetch_cord.fetch.native_module.fetch", side_effect=record):
            NativeProvider().fetch(skip={"cpu", "os"})

        self.assertNotIn("cpu", calls)
        self.assertNotIn("os", calls)
        self.assertIn("kernel", calls)

    def test_returns_nothing_off_windows(self) -> None:
        """native.fetch returns None on other platforms, so the dict is empty."""
        with patch("fetch_cord.fetch.native_module.fetch", return_value=None):
            self.assertEqual(NativeProvider().fetch(), {})

    def test_collecting_natively_runs_no_subprocess(self) -> None:
        """The point of the native path: no tool dependency, no shelling out."""
        with (
            patch("fetch_cord.fetch.native_module.fetch", return_value="value"),
            patch.object(subprocess, "run") as run,
            patch.object(subprocess, "Popen") as popen,
            patch.object(subprocess, "check_output") as check_output,
        ):
            NativeProvider().fetch()

        run.assert_not_called()
        popen.assert_not_called()
        check_output.assert_not_called()


class TestNativeFirstWithFastfetchFallback(unittest.TestCase):
    """Native runs first; fastfetch covers whatever native has not implemented."""

    def test_native_wins_and_fastfetch_fills_the_gaps(self) -> None:
        from fetch_cord.fetch import Fetch

        native = MagicMock()
        native.fetch.return_value = {"cpu": "from native"}
        fastfetch = MagicMock()
        fastfetch.fetch.return_value = {
            "cpu": "from fastfetch",
            "gpu": "from fastfetch",
        }

        data = Fetch([native, fastfetch]).snapshot()

        self.assertEqual(data["cpu"], "from native")
        self.assertEqual(data["gpu"], "from fastfetch")

    def test_a_field_native_cannot_read_falls_through(self) -> None:
        """The safety property: native omits what it is unsure of, so nothing
        is lost by putting it first."""
        from fetch_cord.fetch import Fetch

        fastfetch = MagicMock()
        fastfetch.fetch.return_value = {"os": "from fastfetch"}

        with patch("fetch_cord.fetch.native_module.fetch", return_value=None):
            data = Fetch([NativeProvider(), fastfetch]).snapshot()

        self.assertEqual(data["os"], "from fastfetch")


if __name__ == "__main__":
    unittest.main(verbosity=2)
