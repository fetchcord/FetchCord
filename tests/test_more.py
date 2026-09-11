"""Unit tests for the CLI, update, systemd, native modules and edge cases.

These raise coverage on code paths the main test file doesn't exercise
(CLI argument handling, the self-update logic, systemd integration, the
Windows-native module, and exception paths in cycle/fetch/info/tools).
"""

import argparse
import os
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any
from unittest.mock import MagicMock, patch

from fetch_cord.tools import BashError


class TestArgs(unittest.TestCase):
    def test_parse_args_defaults(self) -> None:
        with patch("sys.argv", ["fetchcord"]):
            from fetch_cord.args import parse_args

            args = parse_args()

        self.assertFalse(args.version)
        self.assertFalse(args.debug)
        self.assertIsNone(args.time)

    def test_parse_args_flags(self) -> None:
        with patch(
            "sys.argv", ["fetchcord", "--version", "-d", "-t", "30", "--nodistro"]
        ):
            from fetch_cord.args import parse_args

            args = parse_args()

        self.assertTrue(args.version)
        self.assertTrue(args.debug)
        self.assertEqual(args.time, "30")
        self.assertTrue(args.nodistro)


class TestUpdate(unittest.TestCase):
    def test_validate_filename(self) -> None:
        from fetch_cord.update import validate_filename

        self.assertTrue(validate_filename("cpus.json"))
        self.assertFalse(validate_filename(""))
        self.assertFalse(validate_filename("../evil.json"))
        self.assertFalse(validate_filename("a/b.json"))
        self.assertFalse(validate_filename("cpus.txt"))

    def test_get_resources_dir(self) -> None:
        from fetch_cord.update import get_resources_dir

        self.assertEqual(get_resources_dir().name, "resources")

    @patch("fetch_cord.update.get_resources_dir")
    @patch("fetch_cord.update.urllib.request.urlretrieve")
    @patch("fetch_cord.update.sys.exit")
    def test_update_success(
        self, mock_exit: MagicMock, mock_urlretrieve: MagicMock, mock_dir: MagicMock
    ) -> None:
        from fetch_cord.constants import RESOURCE_FILES
        from fetch_cord.update import update

        with TemporaryDirectory() as tmp:
            mock_dir.return_value = Path(tmp)
            update(testing=False)

        self.assertEqual(mock_urlretrieve.call_count, len(RESOURCE_FILES))
        mock_exit.assert_called_once_with(0)

    @patch("fetch_cord.update.get_resources_dir")
    @patch("fetch_cord.update.urllib.request.urlretrieve", side_effect=OSError("boom"))
    @patch("fetch_cord.update.sys.exit")
    def test_update_failure(
        self, mock_exit: MagicMock, mock_urlretrieve: MagicMock, mock_dir: MagicMock
    ) -> None:
        from fetch_cord.update import update

        with TemporaryDirectory() as tmp:
            mock_dir.return_value = Path(tmp)
            update(testing=True)

        mock_exit.assert_called_once_with(1)


class TestSystemdService(unittest.TestCase):
    def test_validate_systemd_cmd(self) -> None:
        from fetch_cord.resources import systemd_service as s

        self.assertEqual(s.validate_systemd_cmd(" start "), "start")
        self.assertEqual(s.validate_systemd_cmd("STOP"), "stop")
        with self.assertRaises(ValueError):
            s.validate_systemd_cmd("rm -rf /")
        with self.assertRaises(ValueError):
            s.validate_systemd_cmd("")

    def test_get_service_file_url(self) -> None:
        from fetch_cord.resources import systemd_service as s

        self.assertIn("master", s.get_service_file_url(testing=False))
        self.assertIn("testing", s.get_service_file_url(testing=True))

    @patch("fetch_cord.resources.systemd_service.exec_bash")
    def test_systemd_cmd(self, mock_exec_bash: MagicMock) -> None:
        from fetch_cord.resources import systemd_service as s

        s.systemd_cmd("start")
        mock_exec_bash.assert_called_once()

    @patch("fetch_cord.resources.systemd_service.exec_bash", side_effect=BashError("x"))
    @patch("fetch_cord.resources.systemd_service.sys.exit")
    def test_systemd_cmd_error(
        self, mock_exit: MagicMock, mock_exec_bash: MagicMock
    ) -> None:
        from fetch_cord.resources import systemd_service as s

        s.systemd_cmd("start")
        mock_exit.assert_called_once_with(1)

    @patch("fetch_cord.resources.systemd_service.systemd_cmd")
    @patch("fetch_cord.resources.systemd_service.sys.exit")
    def test_start(self, mock_exit: MagicMock, mock_cmd: MagicMock) -> None:
        from fetch_cord.resources import systemd_service as s

        s.start()
        mock_cmd.assert_called_once_with("start")
        mock_exit.assert_called_once_with(0)

    @patch("fetch_cord.resources.systemd_service.start")
    @patch("fetch_cord.resources.systemd_service.systemd_cmd")
    @patch("fetch_cord.resources.systemd_service.exec_bash")
    @patch("fetch_cord.resources.systemd_service.os.makedirs")
    def test_install(
        self,
        mock_makedirs: MagicMock,
        mock_exec_bash: MagicMock,
        mock_systemd_cmd: MagicMock,
        mock_start: MagicMock,
    ) -> None:
        from fetch_cord.resources import systemd_service as s

        s.install(testing=False)
        mock_exec_bash.assert_called_once()
        mock_systemd_cmd.assert_called_once_with("enable")
        mock_start.assert_called_once()

    @patch("fetch_cord.resources.systemd_service.systemd_cmd")
    @patch("fetch_cord.resources.systemd_service.sys.exit")
    def test_service_commands(self, mock_exit: MagicMock, mock_cmd: MagicMock) -> None:
        from fetch_cord.resources import systemd_service as s

        for name in ("enable", "disable", "stop", "status"):
            with self.subTest(name=name):
                getattr(s, name)()
                mock_cmd.assert_called_with(name)
                mock_exit.assert_called_with(0)

    @patch("fetch_cord.resources.systemd_service.start")
    @patch("fetch_cord.resources.systemd_service.systemd_cmd")
    @patch("fetch_cord.resources.systemd_service.os.makedirs")
    @patch(
        "fetch_cord.resources.systemd_service.exec_bash", side_effect=BashError("dl")
    )
    @patch("fetch_cord.resources.systemd_service.sys.exit")
    def test_install_download_error(
        self,
        mock_exit: MagicMock,
        mock_exec_bash: MagicMock,
        mock_makedirs: MagicMock,
        mock_systemd_cmd: MagicMock,
        mock_start: MagicMock,
    ) -> None:
        from fetch_cord.resources import systemd_service as s

        s.install(testing=False)
        mock_exit.assert_called_once_with(1)

    @patch("fetch_cord.resources.systemd_service.systemd_cmd")
    @patch("fetch_cord.resources.systemd_service.os.path.exists", return_value=True)
    @patch("fetch_cord.resources.systemd_service.os.remove")
    @patch("fetch_cord.resources.systemd_service.sys.exit")
    def test_uninstall(
        self,
        mock_exit: MagicMock,
        mock_remove: MagicMock,
        mock_exists: MagicMock,
        mock_cmd: MagicMock,
    ) -> None:
        from fetch_cord.resources import systemd_service as s

        s.uninstall()
        mock_cmd.assert_any_call("stop")
        mock_cmd.assert_any_call("disable")
        mock_remove.assert_called_once()
        mock_exit.assert_called_once_with(0)

    @patch("fetch_cord.resources.systemd_service.sys.exit")
    def test_systemd_cmd_invalid(self, mock_exit: MagicMock) -> None:
        from fetch_cord.resources import systemd_service as s

        s.systemd_cmd("rm -rf /")  # validate_systemd_cmd raises -> caught -> exit(1)
        mock_exit.assert_called_once_with(1)


class TestNative(unittest.TestCase):
    @patch("fetch_cord.native.native.platform.system")
    def test_native_fetch_unsupported(self, mock_platform: MagicMock) -> None:
        from fetch_cord.native import native as n

        mock_platform.return_value = "Linux"
        self.assertIsNone(n.fetch("packages"))
        mock_platform.return_value = "Darwin"
        self.assertIsNone(n.fetch("packages"))


class TestWindows(unittest.TestCase):
    def test_windows_module_non_nt_fetch(self) -> None:
        """The else-branch returns None off Windows.

        os.name is read at import time, so forcing it means reimporting the
        module rather than just patching the name - otherwise this only ever
        tested whichever branch the test runner happened to be on.
        """
        import importlib

        from fetch_cord.native import Windows as WindowsNative

        with patch("os.name", "posix"):
            reloaded = importlib.reload(WindowsNative)
            try:
                self.assertIsNone(reloaded.fetch("packages"))
            finally:
                importlib.reload(WindowsNative)

    def test_windows_module_nt_fetch_dispatches(self) -> None:
        """And on Windows it dispatches to the packages fetcher."""
        import importlib

        from fetch_cord.native import Windows as WindowsNative

        if os.name != "nt":
            self.skipTest("needs winreg")

        reloaded = importlib.reload(WindowsNative)
        self.assertIsNone(reloaded.fetch("not-a-component"))
        self.assertIn("packages", str(reloaded.fetch("packages")))

    @unittest.skipUnless(os.name == "nt", "winreg is Windows-only")
    def test_get_installed_software(self) -> None:
        from fetch_cord.native.Windows import packages

        fake_winreg = MagicMock()
        fake_winreg.OpenKey.return_value = MagicMock()
        fake_winreg.QueryInfoKey.return_value = (1, 0)
        fake_winreg.EnumKey.return_value = "App1"
        fake_winreg.QueryValueEx.return_value = ("App1 Name", 1)

        # packages imports winreg at module scope, so patching sys.modules
        # after the fact hits the real registry on Windows. Patch the
        # already-bound reference instead.
        with patch.object(packages, "winreg", fake_winreg):
            self.assertEqual(packages.get_installed_software(), ["App1 Name"])
            self.assertEqual(packages.fetch(), "1 packages")


class TestMain(unittest.TestCase):
    def _ns(self, **kwargs: object) -> argparse.Namespace:
        defaults: dict[str, object] = {
            "update": False,
            "testing": False,
            "install": False,
            "uninstall": False,
            "enable": False,
            "disable": False,
            "start": False,
            "stop": False,
            "status": False,
            "version": False,
            "time": None,
            "debug": False,
            "dry_run": False,
            "pause_when": None,
            "nodistro": False,
            "nohardware": False,
            "noshell": False,
            "nohost": False,
        }
        defaults.update(kwargs)
        return argparse.Namespace(**defaults)

    @patch("fetch_cord.__main__.sys.exit")
    @patch("fetch_cord.__main__.print")
    def test_handle_args_version(
        self, mock_print: MagicMock, mock_exit: MagicMock
    ) -> None:
        from fetch_cord.__main__ import handle_args

        handle_args(self._ns(version=True))
        mock_exit.assert_called_once_with(0)

    @patch("fetch_cord.__main__.sys.exit")
    @patch("fetch_cord.__main__.print")
    def test_handle_args_invalid_time(
        self, mock_print: MagicMock, mock_exit: MagicMock
    ) -> None:
        from fetch_cord.__main__ import handle_args

        handle_args(self._ns(time="5"))
        mock_exit.assert_called_once_with(1)

    @patch("fetch_cord.__main__.print")
    def test_handle_args_valid_time(self, mock_print: MagicMock) -> None:
        from fetch_cord.__main__ import handle_args

        handle_args(self._ns(time="30"))
        mock_print.assert_called_once_with("setting custom time 30 seconds")

    @patch("fetch_cord.__main__.print")
    def test_handle_args_fractional_time(self, mock_print: MagicMock) -> None:
        """--time 30.5 used to pass validation then ValueError in main()."""
        from fetch_cord.__main__ import handle_args

        handle_args(self._ns(time="30.5"))
        mock_print.assert_called_once_with("setting custom time 30.5 seconds")

    @patch("fetch_cord.__main__.sys.exit", side_effect=SystemExit)
    @patch("fetch_cord.__main__.print")
    def test_handle_args_non_numeric_time(
        self, mock_print: MagicMock, mock_exit: MagicMock
    ) -> None:
        from fetch_cord.__main__ import handle_args

        with self.assertRaises(SystemExit):
            handle_args(self._ns(time="soon"))
        mock_exit.assert_called_once_with(1)

    @patch("fetch_cord.__main__.update")
    def test_handle_args_update(self, mock_update: MagicMock) -> None:
        from fetch_cord.__main__ import handle_args

        handle_args(self._ns(update=True, testing=True))
        mock_update.assert_called_once_with(testing=True)

    @patch("fetch_cord.__main__.systemd_service.install")
    def test_handle_args_install(self, mock_install: MagicMock) -> None:
        """The systemd flags are gated on os.name AND sys.platform, so pin both.

        Only pinning os.name still skipped the branch on macOS, where
        sys.platform is "darwin".
        """
        from fetch_cord.__main__ import handle_args

        with (
            patch("fetch_cord.__main__.os.name", "posix"),
            patch("fetch_cord.__main__.sys.platform", "linux"),
        ):
            handle_args(self._ns(install=True, testing=False))
        mock_install.assert_called_once_with(testing=False)

    @patch("fetch_cord.__main__.systemd_service.install")
    def test_handle_args_install_ignored_on_windows(
        self, mock_install: MagicMock
    ) -> None:
        from fetch_cord.__main__ import handle_args

        with (
            patch("fetch_cord.__main__.os.name", "nt"),
            patch("fetch_cord.__main__.sys.platform", "win32"),
        ):
            handle_args(self._ns(install=True, testing=False))
        mock_install.assert_not_called()

    @patch("fetch_cord.__main__.systemd_service.install")
    def test_handle_args_install_ignored_on_macos(
        self, mock_install: MagicMock
    ) -> None:
        from fetch_cord.__main__ import handle_args

        with (
            patch("fetch_cord.__main__.os.name", "posix"),
            patch("fetch_cord.__main__.sys.platform", "darwin"),
        ):
            handle_args(self._ns(install=True, testing=False))
        mock_install.assert_not_called()

    @patch("fetch_cord.__main__.Fetch")
    @patch("fetch_cord.presence.get_component_id", return_value="client-1")
    @patch("fetch_cord.__main__.get_infos", return_value={})
    @patch("fetch_cord.cycle.Cycle.try_connect")
    @patch("fetch_cord.cycle.Cycle.update")
    @patch("fetch_cord.cycle.Cycle.setup")
    def test_main_loop(
        self,
        mock_setup: MagicMock,
        mock_update: MagicMock,
        mock_try_connect: MagicMock,
        mock_get_infos: MagicMock,
        mock_get_component_id: MagicMock,
        mock_fetch_class: MagicMock,
    ) -> None:
        from threading import Event, Timer

        from fetch_cord.__main__ import main

        fake_fetch = MagicMock()
        fake_fetch.snapshot.return_value = {
            "os": "Debian",
            "kernel": "6.8",
            "packages": "100",
            "system_type": "desktop",
            "cpu": "AMD",
            "gpu": "NVIDIA",
            "mem": "1 GB",
            "terminal": "xterm",
            "shell": "bash",
            "motherboard": "MB",
            "resolution": "1920x1080",
            "font": "f",
        }
        mock_fetch_class.return_value = fake_fetch

        stop = Event()
        timer = Timer(0.4, stop.set)
        timer.start()
        try:
            main(self._ns(), stop_event=stop)
        finally:
            timer.cancel()

        fake_fetch.snapshot.assert_called()

    @patch("fetch_cord.__main__.Fetch")
    @patch("fetch_cord.presence.get_component_id", return_value="client-1")
    @patch("fetch_cord.__main__.get_infos", return_value={})
    @patch("fetch_cord.cycle.Cycle.try_connect")
    @patch("fetch_cord.cycle.Cycle.setup")
    def test_main_loop_snapshots_once_per_rotation(
        self,
        mock_setup: MagicMock,
        mock_try_connect: MagicMock,
        mock_get_infos: MagicMock,
        mock_get_component_id: MagicMock,
        mock_fetch_class: MagicMock,
    ) -> None:
        """One collection per rotation, not one per cycle.

        Collecting per cycle meant a dozen PowerShell processes four times a
        rotation on Windows, for four reads out of the same data.
        """
        from threading import Event

        from fetch_cord.__main__ import main

        fake_fetch = MagicMock()
        fake_fetch.snapshot.return_value = {}
        mock_fetch_class.return_value = fake_fetch

        stop = Event()
        updates = []

        def record_update(*args: object, **kwargs: object) -> None:
            updates.append(args)
            # Stop once we have been round every cycle exactly once.
            if len(updates) >= 4:
                stop.set()

        with patch("fetch_cord.cycle.Cycle.update", side_effect=record_update):
            main(self._ns(), stop_event=stop)

        self.assertEqual(len(updates), 4)
        self.assertEqual(fake_fetch.snapshot.call_count, 1)


class TestPauseWhenInTheLoop(unittest.TestCase):
    def _ns(self, **kwargs: object) -> argparse.Namespace:
        defaults: dict[str, object] = {
            "update": False,
            "testing": False,
            "install": False,
            "uninstall": False,
            "enable": False,
            "disable": False,
            "start": False,
            "stop": False,
            "status": False,
            "version": False,
            "time": None,
            "debug": False,
            "pause_when": ["steam"],
            "dry_run": False,
            "nodistro": False,
            "nohardware": False,
            "noshell": False,
            "nohost": False,
        }
        defaults.update(kwargs)
        return argparse.Namespace(**defaults)

    @patch("fetch_cord.processes.running_names", return_value=["steam.exe"])
    @patch("fetch_cord.__main__.Fetch")
    @patch("fetch_cord.__main__.get_infos", return_value={})
    @patch("fetch_cord.cycle.Cycle.close_connection")
    @patch("fetch_cord.cycle.Cycle.update")
    @patch("fetch_cord.cycle.Cycle.setup")
    def test_a_paused_program_stops_us_updating(
        self,
        mock_setup: MagicMock,
        mock_update: MagicMock,
        mock_close: MagicMock,
        mock_get_infos: MagicMock,
        mock_fetch_class: MagicMock,
        mock_names: MagicMock,
    ) -> None:
        """The whole point: leave the profile to whatever else is running."""
        from threading import Event

        from fetch_cord.__main__ import main

        fake_fetch = MagicMock()
        fake_fetch.snapshot.return_value = {}
        mock_fetch_class.return_value = fake_fetch

        stop = Event()
        waits: list[object] = []

        def record_wait(*args: object, **kwargs: object) -> None:
            waits.append(args)
            if len(waits) >= 4:
                stop.set()

        with patch("fetch_cord.cycle.Cycle.wait", side_effect=record_wait):
            main(self._ns(), stop_event=stop)

        mock_update.assert_not_called()
        mock_setup.assert_not_called()
        # Nothing to send means nothing to collect: a snapshot is a dozen
        # PowerShell processes on Windows, and pausing is meant to get out
        # of the way, not just stay quiet.
        fake_fetch.snapshot.assert_not_called()
        # It still paces itself rather than spinning.
        self.assertGreaterEqual(len(waits), 4)

    @patch("fetch_cord.processes.running_names", return_value=["firefox"])
    @patch("fetch_cord.__main__.Fetch")
    @patch("fetch_cord.presence.get_component_id", return_value="client-1")
    @patch("fetch_cord.__main__.get_infos", return_value={})
    @patch("fetch_cord.cycle.Cycle.try_connect")
    @patch("fetch_cord.cycle.Cycle.setup")
    def test_nothing_matching_leaves_the_loop_alone(
        self,
        mock_setup: MagicMock,
        mock_try_connect: MagicMock,
        mock_get_infos: MagicMock,
        mock_get_component_id: MagicMock,
        mock_fetch_class: MagicMock,
        mock_names: MagicMock,
    ) -> None:
        from threading import Event

        from fetch_cord.__main__ import main

        fake_fetch = MagicMock()
        fake_fetch.snapshot.return_value = {}
        mock_fetch_class.return_value = fake_fetch

        stop = Event()
        updates: list[object] = []

        def record_update(*args: object, **kwargs: object) -> None:
            updates.append(args)
            if len(updates) >= 2:
                stop.set()

        with patch("fetch_cord.cycle.Cycle.update", side_effect=record_update):
            main(self._ns(), stop_event=stop)

        self.assertGreaterEqual(len(updates), 2)


class TestDryRun(unittest.TestCase):
    def _ns(self, **kwargs: object) -> argparse.Namespace:
        defaults: dict[str, object] = {
            "update": False,
            "testing": False,
            "install": False,
            "uninstall": False,
            "enable": False,
            "disable": False,
            "start": False,
            "stop": False,
            "status": False,
            "version": False,
            "time": None,
            "debug": False,
            "dry_run": True,
            "pause_when": None,
            "nodistro": False,
            "nohardware": False,
            "noshell": False,
            "nohost": False,
        }
        defaults.update(kwargs)
        return argparse.Namespace(**defaults)

    @patch("fetch_cord.cycle.Presence")
    @patch("fetch_cord.__main__.psutil.boot_time", return_value=1700000000)
    @patch("fetch_cord.__main__.Fetch")
    @patch("fetch_cord.__main__.print")
    def test_dry_run_prints_and_never_touches_discord(
        self,
        mock_print: MagicMock,
        mock_fetch_class: MagicMock,
        mock_boot: MagicMock,
        mock_presence: MagicMock,
    ) -> None:
        """The whole point is that it is safe to run with Discord closed."""
        from threading import Event

        from fetch_cord.__main__ import main

        fake_fetch = MagicMock()
        fake_fetch.snapshot.return_value = {
            "os": "Debian GNU/Linux",
            "kernel": "6.8",
            "packages": "100",
            "system_type": "desktop",
            "cpu": "AMD",
            "gpu": "NVIDIA",
            "mem": "1 GB",
            "terminal": "xterm",
            "shell": "bash",
            "motherboard": "MB",
            "resolution": "1920x1080",
            "font": "f",
        }
        mock_fetch_class.return_value = fake_fetch

        main(self._ns(), stop_event=Event())

        mock_presence.assert_not_called()
        printed = "\n".join(str(call) for call in mock_print.call_args_list)
        self.assertIn("Would send", printed)
        self.assertIn("client_id", printed)

    @patch("fetch_cord.__main__.psutil.boot_time", return_value=1700000000)
    @patch("fetch_cord.__main__.print")
    def test_print_dry_run_renders_every_cycle(
        self, mock_print: MagicMock, mock_boot: MagicMock
    ) -> None:
        from fetch_cord.__main__ import print_dry_run
        from fetch_cord.presence import ResolvedCycle

        print_dry_run(
            [
                ResolvedCycle(
                    name="os",
                    client_id="123",
                    app="Debian",
                    top="6.8",
                    bottom="100 packages",
                    icon="Desktop",
                    icon_id="desktop",
                    large_image="big",
                )
            ],
            1700000000,
        )

        printed = "\n".join(str(call) for call in mock_print.call_args_list)
        self.assertIn("cycle: os", printed)
        self.assertIn("123", printed)
        self.assertIn("Debian", printed)


class TestCycleExtras(unittest.TestCase):
    def _cycle(self: Any) -> Any:
        from threading import Event

        from fetch_cord.cycle import Cycle

        return Cycle(
            {
                "name": "t",
                "app_id": "1",
                "top_line": "k",
                "bottom_line": "p",
                "small_icon": "g",
                "time": 30,
            },
            Event(),
        )

    @patch("fetch_cord.cycle.Presence")
    def test_try_connect_retries_then_succeeds(
        self, mock_presence_class: MagicMock
    ) -> None:
        from pypresence import exceptions

        mock_presence = MagicMock()
        mock_presence.connect.side_effect = [exceptions.DiscordNotFound(), None]
        mock_presence_class.return_value = mock_presence

        cycle = self._cycle()
        cycle.rpc = mock_presence
        cycle.wait = MagicMock()

        cycle.try_connect()

        self.assertEqual(mock_presence.connect.call_count, 2)
        cycle.wait.assert_called_once()

    @patch("fetch_cord.cycle.Presence")
    def test_try_connect_is_a_no_op_once_connected(
        self, mock_presence_class: MagicMock
    ) -> None:
        """The main loop calls try_connect every pass; only the first connects.

        Reconnecting an already-connected pipe every pass is what makes a
        single-cycle setup blink.
        """
        mock_presence = MagicMock()
        mock_presence_class.return_value = mock_presence

        cycle = self._cycle()
        cycle.setup("123")

        cycle.try_connect()
        cycle.try_connect()
        cycle.try_connect()

        mock_presence.connect.assert_called_once()

    @patch("fetch_cord.cycle.Presence")
    def test_close_connection_allows_reconnecting(
        self, mock_presence_class: MagicMock
    ) -> None:
        mock_presence = MagicMock()
        mock_presence_class.return_value = mock_presence

        cycle = self._cycle()
        cycle.setup("123")
        cycle.try_connect()
        cycle.close_connection()

        self.assertFalse(cycle.connected)

        cycle.setup("456")
        cycle.try_connect()

        self.assertEqual(mock_presence.connect.call_count, 2)

    @patch("fetch_cord.cycle.psutil")
    @patch("fetch_cord.cycle.Presence")
    def test_update_connection_reset(
        self, mock_presence_class: MagicMock, mock_psutil: MagicMock
    ) -> None:
        mock_presence = MagicMock()
        mock_presence.update.side_effect = ConnectionResetError("reset")
        mock_presence_class.return_value = mock_presence

        cycle = self._cycle()
        cycle.rpc = mock_presence
        cycle.close_connection = MagicMock()

        with self.assertRaises(ConnectionResetError):
            cycle.update("app", "bottom", "top", "icon", "icon_id")

        cycle.close_connection.assert_called_once()

    @patch("fetch_cord.cycle.Presence")
    def test_update_invalid_id(self, mock_presence_class: MagicMock) -> None:
        from pypresence import exceptions

        mock_presence = MagicMock()
        mock_presence.update.side_effect = exceptions.InvalidID()
        mock_presence_class.return_value = mock_presence

        cycle = self._cycle()
        cycle.rpc = mock_presence
        cycle.close_connection = MagicMock()

        with self.assertRaises(exceptions.InvalidID):
            cycle.update("app", "bottom", "top", "icon", "icon_id")

        cycle.close_connection.assert_called_once()

    def test_update_no_rpc_returns_early(self) -> None:
        cycle = self._cycle()
        cycle.rpc = None
        cycle.update("a", "b", "c", "d", "e")  # must not raise

    @patch("fetch_cord.cycle.Presence")
    def test_close_connection_handles_errors(
        self, mock_presence_class: MagicMock
    ) -> None:
        mock_presence = MagicMock()
        mock_presence.clear.side_effect = Exception("clear failed")
        mock_presence.close.side_effect = Exception("close failed")
        mock_presence_class.return_value = mock_presence

        cycle = self._cycle()
        cycle.rpc = mock_presence

        cycle.close_connection()  # must not raise
        self.assertIsNone(cycle.rpc)


class TestFetchExtras(unittest.TestCase):
    def test_get_component_id_no_match(self) -> None:
        from fetch_cord.fetch import get_component_id

        with patch("fetch_cord.fetch.print"):
            result = get_component_id("xyz", {"a": ["b"]})
        self.assertEqual(result, "unknown")

    def test_get_infos(self) -> None:
        from fetch_cord.fetch import get_infos

        data = get_infos("cpus")
        self.assertIsInstance(data, dict)
        self.assertGreater(len(data), 0)

    @patch("fetch_cord.fetch.run_command", return_value="")
    def test_fastfetch_provider_empty(self, mock_run: MagicMock) -> None:
        from fetch_cord.fetch import FastfetchProvider

        self.assertEqual(FastfetchProvider().fetch(), {})


class TestBoardIdentification(unittest.TestCase):
    """The Windows board string has to carry the model, not just the vendor."""

    def test_windows_motherboard_command_reports_vendor_and_product(self) -> None:
        from fetch_cord.config import Config

        windows = Config("fetchcord_cmds.yml")["commands"]["motherboard"]["Windows"]

        self.assertIn("Manufacturer", windows)
        self.assertIn("Product", windows)

    def test_all_platforms_report_a_board_model(self) -> None:
        """Linux already returned board_vendor + board_name; match it."""
        from fetch_cord.config import Config

        commands = Config("fetchcord_cmds.yml")["commands"]["motherboard"]

        self.assertIn("board_name", commands["Linux"])
        self.assertIn("Product", commands["Windows"])

    @patch("builtins.print")
    def test_board_model_can_reach_a_more_specific_id(self, _print: MagicMock) -> None:
        """A vendor-only string can only ever match the vendor's own entry.

        With the board model present, boards that have their own Discord app
        (TUF here) resolve to it instead of the generic vendor one.
        """
        from fetch_cord.fetch import get_component_id, get_infos

        ids = get_infos("motherboards")

        vendor_only = get_component_id("asustek computer inc.", ids)
        with_board = get_component_id("asustek computer inc. tuf gaming b550m", ids)

        self.assertNotEqual(vendor_only, with_board)

    @patch("builtins.print")
    def test_vendor_still_matches_when_the_model_is_unknown(
        self, _print: MagicMock
    ) -> None:
        """Adding the model must not cost us the vendor fallback."""
        from fetch_cord.fetch import get_component_id, get_infos

        ids = get_infos("motherboards")

        self.assertEqual(
            get_component_id("asustek computer inc.", ids),
            get_component_id("asustek computer inc. prime b760-plus d4", ids),
        )


class TestUnknownComponentWarning(unittest.TestCase):
    def setUp(self) -> None:
        from fetch_cord import fetch as fetch_module

        self._warned = fetch_module._WARNED_UNKNOWN
        self._warned.clear()
        self.addCleanup(self._warned.clear)

    @patch("builtins.print")
    def test_unknown_component_warns_only_once(self, mock_print: MagicMock) -> None:
        from fetch_cord.fetch import get_component_id

        for _ in range(5):
            get_component_id("some unlisted gpu", {"known": ["nvidia"]})

        warnings = [
            call for call in mock_print.call_args_list if "No match found" in str(call)
        ]
        self.assertEqual(len(warnings), 1)

    @patch("builtins.print")
    def test_each_distinct_component_still_warns(self, mock_print: MagicMock) -> None:
        from fetch_cord.fetch import get_component_id

        get_component_id("unlisted gpu", {"known": ["nvidia"]})
        get_component_id("unlisted mobo", {"known": ["nvidia"]})

        warnings = [
            call for call in mock_print.call_args_list if "No match found" in str(call)
        ]
        self.assertEqual(len(warnings), 2)


class TestInfoExtras(unittest.TestCase):
    def test_first_text_fallback(self) -> None:
        from fetch_cord.info import _first_text

        self.assertEqual(_first_text({"foo": "bar"}), "bar")
        self.assertEqual(_first_text({"n": 5}), "")

    def test_memory_missing_fields(self) -> None:
        from fetch_cord.info import _format_module

        self.assertEqual(_format_module("Memory", {}), "0.00 GB / 0.00 GB")

    def test_format_module_fallbacks(self) -> None:
        from fetch_cord.info import _format_module

        self.assertEqual(_format_module("OS", {"name": "Ubuntu"}), "Ubuntu")
        self.assertEqual(_format_module("Kernel", {"name": "Linux"}), "Linux")
        self.assertEqual(_format_module("Packages", {"all": 42}), "42")


class TestToolsExtras(unittest.TestCase):
    @patch("fetch_cord.tools.subprocess.run")
    def test_run_command_without_shell(self, mock_run: MagicMock) -> None:
        mock_process = MagicMock()
        mock_process.stdout = "ls output"
        mock_run.return_value = mock_process

        from fetch_cord.tools import run_command

        self.assertEqual(run_command(["ls", "-la"]), "ls output")


if __name__ == "__main__":
    unittest.main(verbosity=2)
