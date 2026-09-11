"""Tests for cross-platform autostart.

Every backend is exercised on every platform by pointing the paths at a temp
directory and injecting a fake winreg, so the CI matrix actually covers all
three rather than only the one it happens to be running on.
"""

import os
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, patch

from fetch_cord import autostart
from fetch_cord.autostart import UnsupportedPlatformError, handle, launcher


class TestLauncher(unittest.TestCase):
    @patch("fetch_cord.autostart.platform.system", return_value="Linux")
    @patch("fetch_cord.autostart.shutil.which", return_value="/usr/bin/fetchcord")
    def test_prefers_the_installed_console_script(
        self, mock_which: MagicMock, mock_system: MagicMock
    ) -> None:
        self.assertEqual(launcher(), ["/usr/bin/fetchcord"])

    @patch("fetch_cord.autostart.platform.system", return_value="Linux")
    @patch("fetch_cord.autostart.shutil.which", return_value=None)
    def test_falls_back_to_the_current_interpreter(
        self, mock_which: MagicMock, mock_system: MagicMock
    ) -> None:
        """A venv or pipx install may not have the script on PATH at login."""
        self.assertEqual(launcher(), [sys.executable, "-m", "fetch_cord"])

    @patch("fetch_cord.autostart.platform.system", return_value="Windows")
    @patch("fetch_cord.autostart.shutil.which")
    def test_windows_prefers_the_windowless_launcher(
        self, mock_which: MagicMock, mock_system: MagicMock
    ) -> None:
        """Otherwise a console window flashes up at every sign-in."""
        mock_which.side_effect = lambda name: (
            r"C:\Scripts\fetchcordw.exe" if name == "fetchcordw" else None
        )

        self.assertEqual(launcher(), [r"C:\Scripts\fetchcordw.exe"])

    def test_quoting_only_quotes_what_needs_it(self) -> None:
        self.assertEqual(
            autostart._quote([r"C:\Program Files\fetchcord.exe", "-m"]),
            r'"C:\Program Files\fetchcord.exe" -m',
        )


class _TempPathMixin(unittest.TestCase):
    def setUp(self) -> None:
        self._dir = tempfile.TemporaryDirectory()
        self.addCleanup(self._dir.cleanup)
        self.path = os.path.join(self._dir.name, "nested", "fetchcord.file")


class TestMacOSBackend(_TempPathMixin):
    def setUp(self) -> None:
        super().setUp()
        patcher = patch("fetch_cord.autostart.agent_path", return_value=self.path)
        patcher.start()
        self.addCleanup(patcher.stop)
        bash = patch("fetch_cord.autostart._try_bash", return_value=True)
        self.bash = bash.start()
        self.addCleanup(bash.stop)

    def test_install_writes_a_plist_naming_the_launcher(self) -> None:
        autostart._macos_install()

        with open(self.path, encoding="utf-8") as handle:
            plist = handle.read()

        self.assertIn("<key>RunAtLoad</key>", plist)
        self.assertIn(autostart.AGENT_LABEL, plist)
        for part in launcher():
            self.assertIn(f"<string>{part}</string>", plist)

    def test_round_trip(self) -> None:
        self.assertIsNone(autostart._macos_status())
        autostart._macos_install()
        self.assertIsNotNone(autostart._macos_status())
        self.assertTrue(autostart._macos_uninstall())
        self.assertIsNone(autostart._macos_status())

    def test_uninstalling_when_absent_reports_nothing_removed(self) -> None:
        self.assertFalse(autostart._macos_uninstall())


class TestLinuxBackend(_TempPathMixin):
    def setUp(self) -> None:
        super().setUp()
        patcher = patch("fetch_cord.autostart.unit_path", return_value=self.path)
        patcher.start()
        self.addCleanup(patcher.stop)
        bash = patch("fetch_cord.autostart._try_bash", return_value=True)
        self.bash = bash.start()
        self.addCleanup(bash.stop)

    def test_install_writes_a_unit_naming_the_launcher(self) -> None:
        autostart._linux_install()

        with open(self.path, encoding="utf-8") as handle:
            unit = handle.read()

        self.assertIn("[Service]", unit)
        self.assertIn("WantedBy=default.target", unit)
        self.assertIn(autostart._quote(launcher()), unit)

    def test_round_trip(self) -> None:
        self.assertIsNone(autostart._linux_status())
        autostart._linux_install()
        self.assertIsNotNone(autostart._linux_status())
        self.assertTrue(autostart._linux_uninstall())
        self.assertIsNone(autostart._linux_status())

    def test_a_machine_without_systemd_still_gets_the_unit(self) -> None:
        """systemctl missing is not a reason to fail the install."""
        self.bash.return_value = False

        autostart._linux_install()

        self.assertTrue(os.path.exists(self.path))


class TestWindowsBackend(unittest.TestCase):
    """winreg is imported inside each function, so a fake can be injected."""

    def setUp(self) -> None:
        self.winreg = MagicMock()
        self.winreg.HKEY_CURRENT_USER = 0
        patcher = patch.dict(sys.modules, {"winreg": self.winreg})
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_install_writes_the_run_key(self) -> None:
        command = autostart._windows_install()

        self.winreg.CreateKeyEx.assert_called_once()
        self.winreg.SetValueEx.assert_called_once()
        self.assertEqual(
            self.winreg.SetValueEx.call_args[0][4], autostart._quote(launcher())
        )
        self.assertEqual(command, autostart._quote(launcher()))

    def test_status_reads_the_run_key(self) -> None:
        self.winreg.QueryValueEx.return_value = ("fetchcord.exe", 1)

        self.assertEqual(autostart._windows_status(), "fetchcord.exe")

    def test_status_is_none_when_the_value_is_absent(self) -> None:
        self.winreg.OpenKey.side_effect = OSError

        self.assertIsNone(autostart._windows_status())

    def test_uninstall_reports_when_there_was_nothing_to_remove(self) -> None:
        self.winreg.OpenKey.side_effect = OSError

        self.assertFalse(autostart._windows_uninstall())

    def test_uninstall_deletes_the_value(self) -> None:
        self.assertTrue(autostart._windows_uninstall())
        self.winreg.DeleteValue.assert_called_once()


class TestDispatch(unittest.TestCase):
    @patch("fetch_cord.autostart.platform.system", return_value="Haiku")
    def test_an_unsupported_platform_raises(self, mock_system: MagicMock) -> None:
        with self.assertRaises(UnsupportedPlatformError):
            autostart.status()

    @patch("fetch_cord.autostart.platform.system", return_value="Haiku")
    @patch("builtins.print")
    def test_handle_reports_an_unsupported_platform_as_a_failure(
        self, mock_print: MagicMock, mock_system: MagicMock
    ) -> None:
        self.assertEqual(handle("install"), 1)

    @patch("fetch_cord.autostart.install", return_value="/tmp/unit")
    @patch("builtins.print")
    def test_handle_install(
        self, mock_print: MagicMock, mock_install: MagicMock
    ) -> None:
        self.assertEqual(handle("install"), 0)
        self.assertIn("Autostart enabled", str(mock_print.call_args))

    @patch("fetch_cord.autostart.uninstall", return_value=False)
    @patch("builtins.print")
    def test_handle_uninstall_when_absent(
        self, mock_print: MagicMock, mock_uninstall: MagicMock
    ) -> None:
        self.assertEqual(handle("uninstall"), 0)
        self.assertIn("was not configured", str(mock_print.call_args))

    @patch("fetch_cord.autostart.status", return_value=None)
    @patch("builtins.print")
    def test_handle_status_when_off(
        self, mock_print: MagicMock, mock_status: MagicMock
    ) -> None:
        self.assertEqual(handle("status"), 0)
        self.assertIn("off", str(mock_print.call_args))

    @patch("fetch_cord.autostart.install", side_effect=OSError("read-only"))
    @patch("builtins.print")
    def test_handle_turns_an_os_error_into_an_exit_code(
        self, mock_print: MagicMock, mock_install: MagicMock
    ) -> None:
        """A locked-down machine should get a message, not a traceback."""
        self.assertEqual(handle("install"), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
