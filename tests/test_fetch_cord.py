#!/usr/bin/env python3
"""Test suite for FetchCord modules.

Tests cover:
- Config: YAML configuration loading
- Cycle: Discord RPC cycle management
- Fetch: System information fetching
- Tools: Command execution utilities
"""

import json
import os
import subprocess
import sys
import unittest
from threading import Event
from typing import Any
from unittest.mock import MagicMock, mock_open, patch

from fetch_cord.tools import COMMAND_TIMEOUT_SECONDS


class TestConfig(unittest.TestCase):
    """Test cases for Config class."""

    @patch("fetch_cord.config.get_resource_path", return_value="/fake/path/config.yml")
    @patch("fetch_cord.config.yaml.safe_load")
    @patch("builtins.open", new_callable=mock_open, read_data="key: value")
    def test_config_loads_yaml(self, mock_file, mock_yaml_load, mock_resources_path):
        """Test that Config loads YAML configuration correctly."""
        mock_resources_path.return_value = "/fake/path/config.yml"
        mock_yaml_load.return_value = {"key": "value", "nested": {"data": 123}}

        from fetch_cord.config import Config

        config = Config("fetchcord_conf.yml")

        self.assertEqual(config["key"], "value")
        self.assertEqual(config["nested"]["data"], 123)

    @patch("fetch_cord.config.get_resource_path", return_value="/fake/path/config.yml")
    @patch("fetch_cord.config.yaml.safe_load")
    @patch("builtins.open", new_callable=mock_open, read_data="key: value")
    def test_config_acts_like_dict(
        self, mock_file, mock_yaml_load, mock_resources_path
    ):
        """Test that Config behaves like a dictionary."""
        mock_resources_path.return_value = "/fake/path/config.yml"
        mock_yaml_load.return_value = {"key": "value", "number": 42}

        from fetch_cord.config import Config

        config = Config()

        self.assertIn("key", config)
        self.assertEqual(len(config), 2)
        self.assertEqual(list(config.keys()), ["key", "number"])

    @patch("fetch_cord.config.get_resource_path", return_value="/fake/path/config.yml")
    @patch("fetch_cord.config.yaml.safe_load")
    @patch("builtins.open", new_callable=mock_open, read_data="key: value")
    def test_config_default_config_name(
        self, mock_file, mock_yaml_load, mock_resources_path
    ):
        """Test that Config uses default config name when not specified."""
        mock_resources_path.return_value = "/fake/path/config.yml"
        mock_yaml_load.return_value = {"test": "data"}

        from fetch_cord.config import Config

        Config()

        mock_resources_path.assert_called_once()
        args = mock_resources_path.call_args[0]
        self.assertEqual(args[1], "fetchcord_conf.yml")

    @patch("fetch_cord.config.get_resource_path", return_value="/fake/path/config.yml")
    @patch("fetch_cord.config.print")
    @patch("builtins.open", new_callable=mock_open, read_data="key: value")
    def test_config_yaml_error_handling(
        self, mock_file, mock_print, mock_resources_path
    ):
        """Test that Config handles YAML errors gracefully."""
        import yaml

        mock_resources_path.return_value = "/fake/path/config.yml"

        from fetch_cord.config import Config

        with (
            patch.object(yaml, "safe_load", side_effect=yaml.YAMLError("YAML Error")),
            self.assertRaises(ValueError),
        ):
            Config()


class TestCycle(unittest.TestCase):
    """Test cases for Cycle class."""

    def setUp(self):
        """Set up test fixtures."""
        self.config = {
            "name": "test_cycle",
            "app_id": "123456789",
            "top_line": "Top Line",
            "bottom_line": "Bottom Line",
            "small_icon": "icon_name",
            "time": "30",
            "debug": True,
        }

    @patch("fetch_cord.cycle.Presence")
    def test_cycle_initialization(self, mock_presence_class):
        """Test Cycle initialization with config."""
        from fetch_cord.cycle import Cycle

        stop_event = Event()
        cycle = Cycle(self.config, stop_event)

        self.assertEqual(cycle.name, "test_cycle")
        self.assertEqual(cycle.app_id, "123456789")
        self.assertEqual(cycle.top_line, "Top Line")
        self.assertEqual(cycle.bottom_line, "Bottom Line")
        self.assertEqual(cycle.small_icon, "icon_name")
        self.assertEqual(cycle.time, "30")
        self.assertTrue(cycle.debug)
        self.assertEqual(cycle.stop, stop_event)

    @patch("fetch_cord.cycle.Presence")
    def test_cycle_default_stop_event(self, mock_presence_class):
        """Test Cycle creates default stop event if none provided."""
        from fetch_cord.cycle import Cycle

        cycle = Cycle(self.config)

        self.assertIsNotNone(cycle.stop)
        self.assertIsInstance(cycle.stop, Event)

    @patch("fetch_cord.cycle.Presence")
    def test_cycle_setup(self, mock_presence_class):
        """Test Cycle setup method."""
        mock_presence = MagicMock()
        mock_presence_class.return_value = mock_presence

        from fetch_cord.cycle import Cycle

        cycle = Cycle(self.config)
        cycle.setup("123456")

        mock_presence_class.assert_called_once_with(123456)
        self.assertEqual(cycle.rpc, mock_presence)

    @patch("fetch_cord.cycle.Presence")
    def test_cycle_try_connect_success(self, mock_presence_class):
        """Test Cycle try_connect succeeds immediately."""
        mock_presence = MagicMock()
        mock_presence.connect = MagicMock()
        mock_presence_class.return_value = mock_presence

        from fetch_cord.cycle import Cycle

        cycle = Cycle(self.config)
        cycle.setup("123456")
        cycle.try_connect()

        mock_presence.connect.assert_called_once()

    @patch("fetch_cord.cycle.Presence")
    @patch("fetch_cord.cycle.print")
    def test_cycle_try_connect_refused(self, mock_print, mock_presence_class):
        """Test Cycle try_connect handles ConnectionRefusedError."""
        mock_presence = MagicMock()
        mock_presence.connect.side_effect = [
            ConnectionRefusedError(),
            ConnectionRefusedError(),
            None,
        ]
        mock_presence_class.return_value = mock_presence

        from fetch_cord.cycle import Cycle

        stop_event = Event()
        cycle = Cycle(self.config, stop_event)
        cycle.setup("123456")
        cycle.wait = MagicMock()
        cycle.try_connect()

        self.assertGreater(mock_presence.connect.call_count, 1)

    @patch("fetch_cord.cycle.psutil")
    @patch("fetch_cord.cycle.Presence")
    def test_cycle_update(self, mock_presence_class, mock_psutil):
        """Test Cycle update method."""
        mock_presence = MagicMock()
        mock_presence.update = MagicMock()
        mock_presence.close = MagicMock()
        mock_presence_class.return_value = mock_presence
        mock_psutil.boot_time.return_value = 1234567890

        from fetch_cord.cycle import Cycle

        cycle = Cycle(self.config)
        cycle.setup("123456")
        cycle.wait = MagicMock()

        cycle.update("App Name", "Bottom Text", "Top Text", "Icon", "icon_id")

        mock_presence.update.assert_called_once_with(
            state="Bottom Text",
            details="Top Text",
            large_image="big",
            large_text="App Name",
            small_image="icon_id",
            small_text="Icon",
            start=1234567890,
        )
        # A successful update keeps the RPC connection open (no close).
        mock_presence.close.assert_not_called()

    @patch("fetch_cord.cycle.Presence")
    def test_cycle_wait(self, mock_presence_class):
        """Test Cycle wait method."""
        from fetch_cord.cycle import Cycle

        stop_event = Event()
        cycle = Cycle(self.config, stop_event)

        stop_event.set()
        cycle.wait(0.1)

    @patch("fetch_cord.cycle.Presence")
    def test_cycle_wait_with_interval(self, mock_presence_class):
        """Test Cycle wait method with interval checking."""
        from fetch_cord.cycle import Cycle

        stop_event = Event()
        cycle = Cycle(self.config, stop_event)

        def set_stop():
            stop_event.set()

        import threading

        timer = threading.Timer(0.05, set_stop)
        timer.start()

        cycle.wait(1.0, interval_duration=0.01)
        timer.join()

    @patch("fetch_cord.cycle.Presence")
    def test_cycle_wait_returns_promptly_when_stopped(self, mock_presence_class):
        """A 30s cycle must not keep the process alive for 30s after Ctrl+C."""
        import time as _time

        from fetch_cord.cycle import Cycle

        stop_event = Event()
        cycle = Cycle(self.config, stop_event)

        import threading

        timer = threading.Timer(0.05, stop_event.set)
        timer.start()
        try:
            started = _time.perf_counter()
            cycle.wait(30)
            elapsed = _time.perf_counter() - started
        finally:
            timer.cancel()

        self.assertLess(elapsed, 5)

    @patch("fetch_cord.cycle.Presence")
    def test_cycle_repr(self, mock_presence_class):
        """Test Cycle __repr__ method."""
        from fetch_cord.cycle import Cycle

        cycle = Cycle(self.config)
        repr_str = repr(cycle)

        self.assertIn("test_cycle", repr_str)
        self.assertIn("123456789", repr_str)
        self.assertIn("Top Line", repr_str)

    @patch("fetch_cord.cycle.Presence")
    def test_cycle_close_connection(self, mock_presence_class):
        """Explicit close_connection releases the RPC client."""
        mock_presence = MagicMock()
        mock_presence.clear = MagicMock()
        mock_presence.close = MagicMock()
        mock_presence_class.return_value = mock_presence

        from fetch_cord.cycle import Cycle

        cycle = Cycle(self.config)
        cycle.setup("123456")
        cycle.rpc = mock_presence

        cycle.close_connection()

        mock_presence.clear.assert_called_once()
        mock_presence.close.assert_called_once()
        self.assertIsNone(cycle.rpc)


class TestFetchFunctions(unittest.TestCase):
    """Test cases for Fetch module functions (standalone, no module imports)."""

    def test_get_component_id_exact_match(self):
        """Test get_component_id with exact pattern match."""
        id_list = {
            "intel_cpu": ["Intel.*i7", "Intel.*i5"],
            "amd_cpu": ["AMD.*Ryzen", "AMD.*FX"],
        }

        result = self._call_get_component_id("Intel Core i7-9700K", id_list)
        self.assertEqual(result, "intel_cpu")

    def test_get_component_id_no_match_with_unknown(self):
        """Test get_component_id returns unknown when no match."""
        id_list = {
            "intel_cpu": ["Intel.*i7"],
            "amd_cpu": ["AMD.*Ryzen"],
            "unknown": ["unknown"],
        }

        result = self._call_get_component_id("Some Random CPU", id_list)
        self.assertEqual(result, "unknown")

    def test_get_component_id_no_match_no_unknown(self):
        """Test get_component_id returns 'unknown' string when no match and no unknown pattern."""
        id_list = {
            "intel_cpu": ["Intel.*i7"],
        }

        result = self._call_get_component_id("Some Random CPU", id_list)
        self.assertEqual(result, "unknown")

    def test_get_component_id_case_sensitive(self):
        """Test get_component_id with case sensitivity."""
        id_list = {
            "intel_cpu": ["Intel"],
        }

        result = self._call_get_component_id("intel cpu", id_list)
        self.assertEqual(result, "unknown")

    def _call_get_component_id(self, search, id_list):
        from fetch_cord.fetch import get_component_id

        return get_component_id(search, id_list)

    def test_get_component_id_from_os_db(self):
        from fetch_cord.fetch import get_component_id, get_infos

        os_ids = get_infos("os")
        debian_id = get_component_id("debian gnu/linux 13.4 (trixie)", os_ids)
        self.assertNotEqual(debian_id, "unknown")
        self.assertTrue(debian_id.isdigit())

        macos_id = get_component_id("macos 15.1", os_ids)
        self.assertNotEqual(macos_id, "unknown")


class TestInfo(unittest.TestCase):
    """Tests for the structured fastfetch JSON parser."""

    def test_parse_fastfetch_json_basic(self):
        from fetch_cord.info import parse_fastfetch_json

        raw = json.dumps(
            [
                {
                    "type": "OS",
                    "result": {"prettyName": "Arch Linux", "name": "Arch Linux"},
                },
                {
                    "type": "Kernel",
                    "result": {"release": "6.8.0-arch", "name": "Linux"},
                },
                {"type": "CPU", "result": {"cpu": "AMD Ryzen 9"}},
                {"type": "GPU", "error": "GPU detection failed"},
                {"type": "Memory", "result": {"used": 2147483648, "total": 4294967296}},
                {"type": "Packages", "result": {"all": 100, "pacman": 100}},
            ]
        )

        fields = parse_fastfetch_json(raw)

        self.assertEqual(fields["os"], "Arch Linux")
        self.assertEqual(fields["kernel"], "6.8.0-arch")
        self.assertEqual(fields["cpu"], "AMD Ryzen 9")
        self.assertEqual(fields["memory"], "2.00 GB / 4.00 GB")
        self.assertEqual(fields["packages"], "100")
        self.assertNotIn("gpu", fields)  # error entries are skipped

    def test_parse_fastfetch_json_invalid(self):
        from fetch_cord.info import parse_fastfetch_json

        self.assertEqual(parse_fastfetch_json("not json"), {})
        self.assertEqual(parse_fastfetch_json(""), {})

    def test_parse_fastfetch_json_not_a_list(self):
        from fetch_cord.info import parse_fastfetch_json

        self.assertEqual(parse_fastfetch_json('{"modules": {}}'), {})

    def test_parse_fastfetch_json_memory_zero(self):
        from fetch_cord.info import parse_fastfetch_json

        raw = json.dumps(
            [{"type": "Memory", "result": {"used": 0, "total": 1073741824}}]
        )
        fields = parse_fastfetch_json(raw)
        self.assertEqual(fields["memory"], "0.00 GB / 1.00 GB")

    def test_parse_fastfetch_json_gpu_array(self):
        from fetch_cord.info import parse_fastfetch_json

        raw = json.dumps(
            [
                {
                    "type": "GPU",
                    "result": [
                        {"name": "NVIDIA GeForce RTX 4080", "vendor": "NVIDIA"},
                        {"name": "AMD Radeon", "vendor": "AMD"},
                    ],
                }
            ]
        )
        fields = parse_fastfetch_json(raw)
        self.assertEqual(fields["gpu"], "NVIDIA GeForce RTX 4080 / AMD Radeon")


class TestFetchClass(unittest.TestCase):
    """Tests for the field providers and the Fetch snapshot cache."""

    @classmethod
    def setUpClass(cls):
        cls.native_patcher = patch.dict(
            sys.modules,
            {"fetch_cord.native.native": MagicMock(fetch=MagicMock(return_value=None))},
        )
        cls.native_patcher.start()
        cls.resources_patcher = patch("fetch_cord.fetch.resources")
        cls.mock_resources = cls.resources_patcher.start()
        cls.mock_resources.__file__ = "/fake/resources/__init__.py"

    @classmethod
    def tearDownClass(cls):
        cls.native_patcher.stop()
        cls.resources_patcher.stop()

    @patch("fetch_cord.fetch.run_command")
    def test_fastfetch_provider_parses_output(self, mock_run):
        from fetch_cord.fetch import FastfetchProvider

        mock_run.return_value = json.dumps(
            [{"type": "OS", "result": {"prettyName": "Debian GNU/Linux"}}]
        )
        fields = FastfetchProvider().fetch()
        self.assertEqual(fields["os"], "Debian GNU/Linux")

    @patch("fetch_cord.fetch.run_command", side_effect=FileNotFoundError)
    def test_fastfetch_provider_handles_missing_binary(self, mock_run):
        from fetch_cord.fetch import FastfetchProvider

        self.assertEqual(FastfetchProvider().fetch(), {})

    @patch("fetch_cord.fetch.platform.system", return_value="Linux")
    @patch("fetch_cord.fetch.exec_bash")
    def test_command_provider_skips_existing_and_strips(
        self, mock_exec_bash, mock_system
    ):
        from fetch_cord.fetch import CommandProvider

        mock_exec_bash.return_value = "  Value\nignored line\n"
        provider = CommandProvider({"cpu": "echo cpu", "gpu": "echo gpu"})

        fields = provider.fetch(skip={"cpu"})  # cpu already provided elsewhere

        mock_exec_bash.assert_called_once_with("echo gpu")
        self.assertEqual(fields, {"gpu": "Value"})

    @patch("fetch_cord.fetch.platform.system", return_value="Windows")
    @patch("fetch_cord.fetch.exec_ps1")
    def test_command_provider_uses_powershell_on_windows(
        self, mock_exec_ps1, mock_system
    ):
        """CommandProvider branches on the OS, so the OS has to be pinned."""
        from fetch_cord.fetch import CommandProvider

        mock_exec_ps1.return_value = "  Value\nignored line\n"

        fields = CommandProvider({"gpu": "Get-Gpu"}).fetch()

        mock_exec_ps1.assert_called_once_with("Get-Gpu")
        self.assertEqual(fields, {"gpu": "Value"})

    @patch("fetch_cord.fetch.platform.system", return_value="Linux")
    def test_command_provider_handles_bash_error(self, mock_system):
        from fetch_cord.tools import BashError

        with patch("fetch_cord.fetch.exec_bash", side_effect=BashError("boom")):
            from fetch_cord.fetch import CommandProvider

            self.assertEqual(CommandProvider({"cpu": "bad"}).fetch(), {})

    @patch("fetch_cord.fetch.platform.system", return_value="Windows")
    def test_command_provider_handles_powershell_error(self, mock_system):
        from fetch_cord.tools import BashError

        with patch("fetch_cord.fetch.exec_ps1", side_effect=BashError("boom")):
            from fetch_cord.fetch import CommandProvider

            self.assertEqual(CommandProvider({"cpu": "bad"}).fetch(), {})

    def test_native_provider(self):
        from fetch_cord.fetch import NativeProvider

        provider = NativeProvider()
        provider._native = MagicMock(fetch=MagicMock(return_value="432 packages"))
        fields = provider.fetch()
        self.assertEqual(fields.get("packages"), "432 packages")

    def test_fetch_snapshot_first_provider_wins(self):
        from fetch_cord.fetch import Fetch

        class ProviderOne:
            name = "one"

            def fetch(self, skip=None):
                return {"a": "1", "b": "1"}

        class ProviderTwo:
            name = "two"

            def fetch(self, skip=None):
                # Only fills gaps; must not overwrite existing fields.
                return {"b": "2", "c": "2"}

        fetch = Fetch([ProviderOne(), ProviderTwo()])
        snap = fetch.snapshot()

        self.assertEqual(snap, {"a": "1", "b": "1", "c": "2"})
        self.assertEqual(fetch.fetch("a"), "1")
        self.assertEqual(fetch.fetch("b"), "1")
        self.assertEqual(fetch.fetch("c"), "2")

    def test_fetch_missing_field_returns_not_found(self):
        from fetch_cord.fetch import Fetch

        class EmptyProvider:
            name = "empty"

            def fetch(self, skip=None):
                return {}

        fetch = Fetch([EmptyProvider()])
        self.assertEqual(fetch.fetch("nonexistent"), "Not Found")
        self.assertEqual(fetch.fetch(None), "Not Found")

    def test_snapshot_aliases_memory_to_mem(self):
        from fetch_cord.fetch import Fetch

        class MemProvider:
            name = "mem"

            def fetch(self, skip=None):
                return {"memory": "2.00 GB / 4.00 GB"}

        snap = Fetch([MemProvider()]).snapshot()
        self.assertEqual(snap["memory"], "2.00 GB / 4.00 GB")
        self.assertEqual(snap["mem"], "2.00 GB / 4.00 GB")

    @patch("fetch_cord.fetch.run_command")
    def test_fastfetch_drops_pythonish_terminal(self, mock_run):
        from fetch_cord.fetch import FastfetchProvider

        mock_run.return_value = json.dumps(
            [
                {"type": "OS", "result": {"prettyName": "Debian GNU/Linux"}},
                {"type": "Terminal", "result": {"prettyName": "python"}},
                {"type": "Shell", "result": {"prettyName": "hermes"}},
            ]
        )
        fields = FastfetchProvider().fetch()
        self.assertEqual(fields["os"], "Debian GNU/Linux")
        self.assertNotIn("terminal", fields)
        self.assertNotIn("shell", fields)


class TestTools(unittest.TestCase):
    """Test cases for Tools module."""

    @patch("fetch_cord.tools.subprocess.run")
    def test_run_command(self, mock_run):
        """Test run_command function."""
        mock_process = MagicMock()
        mock_process.stdout = "command output"
        mock_run.return_value = mock_process

        from fetch_cord.tools import run_command

        result = run_command(["ls", "-la"])

        mock_run.assert_called_once_with(
            ["ls", "-la"],
            encoding="utf-8",
            errors="replace",
            stdout=-1,
            stderr=subprocess.DEVNULL,
            timeout=COMMAND_TIMEOUT_SECONDS,
            shell=False,
        )
        self.assertEqual(result, "command output")

    @patch("fetch_cord.tools.subprocess.run")
    def test_run_command_with_shell(self, mock_run):
        """Test run_command with shell=True."""
        mock_process = MagicMock()
        mock_process.stdout = "shell output"
        mock_run.return_value = mock_process

        from fetch_cord.tools import run_command

        run_command(["echo", "hello"], shell=True)

        mock_run.assert_called_once_with(
            ["echo", "hello"],
            encoding="utf-8",
            errors="replace",
            stdout=-1,
            stderr=subprocess.DEVNULL,
            timeout=COMMAND_TIMEOUT_SECONDS,
            shell=True,
        )

    @patch("fetch_cord.tools.subprocess.run")
    def test_exec_bash(self, mock_run):
        """Test exec_bash function."""
        mock_process = MagicMock()
        mock_process.stdout = "  bash output  \n"
        mock_process.returncode = 0
        mock_run.return_value = mock_process

        from fetch_cord.tools import exec_bash

        result = exec_bash("echo hello")

        mock_run.assert_called_once_with(
            "echo hello",
            encoding="utf-8",
            capture_output=True,
            timeout=COMMAND_TIMEOUT_SECONDS,
            shell=True,
        )
        self.assertEqual(result, "bash output")

    @patch("fetch_cord.tools.subprocess.run")
    def test_exec_bash_raises_on_failure(self, mock_run):
        """exec_bash raises BashError when the command exits non-zero."""
        mock_process = MagicMock()
        mock_process.stdout = "some error"
        mock_process.returncode = 1
        mock_run.return_value = mock_process

        from fetch_cord.tools import BashError, exec_bash

        with self.assertRaises(BashError):
            exec_bash("false")

    @patch("fetch_cord.tools.subprocess.run")
    def test_exec_ps1(self, mock_run):
        """Test exec_ps1 function."""
        mock_process = MagicMock()
        mock_process.stdout = "  powershell output  \n"
        mock_process.returncode = 0
        mock_run.return_value = mock_process

        from fetch_cord.tools import exec_ps1

        result = exec_ps1("Get-Process")

        from fetch_cord.tools import PS1_PREAMBLE

        mock_run.assert_called_once_with(
            [
                "powershell",
                "-NoProfile",
                "-NonInteractive",
                "-Command",
                PS1_PREAMBLE + "Get-Process",
            ],
            encoding="utf-8",
            errors="replace",
            capture_output=True,
            timeout=COMMAND_TIMEOUT_SECONDS,
        )
        self.assertEqual(result, "powershell output")

    @unittest.skipUnless(os.name == "nt", "PowerShell is Windows-only")
    def test_exec_ps1_non_ascii_output_does_not_raise(self):
        """Non-ASCII output must come back decoded, not as a UnicodeDecodeError.

        Regression test: PowerShell 5.1 emits the console OEM code page, so
        decoding its bytes as UTF-8 used to blow up on any accented character
        - and UnicodeDecodeError is not a BashError, so it escaped
        CommandProvider's handler and killed the presence loop.
        """
        from fetch_cord.tools import exec_ps1

        self.assertEqual(exec_ps1("Write-Output 'Ünïcödé — ok'"), "Ünïcödé — ok")

    @patch("fetch_cord.tools.subprocess.run")
    def test_exec_ps1_treats_error_only_output_as_failure(self, mock_run):
        """A non-terminating PowerShell error must not become a field value.

        PowerShell exits 0 after a non-terminating error, and stderr used to
        be merged into stdout - so a command whose only output was an error
        message had that message returned as the value, and it went straight
        onto the user's Discord profile.
        """
        mock_process = MagicMock()
        mock_process.stdout = ""
        mock_process.stderr = "You cannot call a method on a null-valued expression."
        mock_process.returncode = 0
        mock_run.return_value = mock_process

        from fetch_cord.tools import BashError, exec_ps1

        with self.assertRaises(BashError):
            exec_ps1("$null.ToString()")

    @patch("fetch_cord.tools.subprocess.run")
    def test_exec_ps1_keeps_stderr_out_of_the_value(self, mock_run):
        """Output plus a warning still yields just the output."""
        mock_process = MagicMock()
        mock_process.stdout = "2560x1440\n"
        mock_process.stderr = "WARNING: something noisy"
        mock_process.returncode = 0
        mock_run.return_value = mock_process

        from fetch_cord.tools import exec_ps1

        self.assertEqual(exec_ps1("Get-Resolution"), "2560x1440")

    @patch("fetch_cord.tools.subprocess.run")
    def test_exec_bash_keeps_stderr_out_of_the_value(self, mock_run):
        mock_process = MagicMock()
        mock_process.stdout = "1920x1080\n"
        mock_process.stderr = "xdpyinfo: warning"
        mock_process.returncode = 0
        mock_run.return_value = mock_process

        from fetch_cord.tools import exec_bash

        self.assertEqual(exec_bash("xdpyinfo"), "1920x1080")

    @patch("fetch_cord.tools.subprocess.run")
    def test_exec_bash_timeout_raises_bash_error(self, mock_run):
        """A wedged command becomes a BashError instead of hanging forever."""
        mock_run.side_effect = subprocess.TimeoutExpired(
            cmd="sleep 999", timeout=COMMAND_TIMEOUT_SECONDS
        )

        from fetch_cord.tools import BashError, exec_bash

        with self.assertRaises(BashError):
            exec_bash("sleep 999")

    @patch("fetch_cord.tools.subprocess.run")
    def test_exec_ps1_timeout_raises_bash_error(self, mock_run):
        mock_run.side_effect = subprocess.TimeoutExpired(
            cmd="Start-Sleep", timeout=COMMAND_TIMEOUT_SECONDS
        )

        from fetch_cord.tools import BashError, exec_ps1

        with self.assertRaises(BashError):
            exec_ps1("Start-Sleep 999")

    @patch("fetch_cord.tools.subprocess.run")
    def test_run_command_timeout_raises_bash_error(self, mock_run):
        mock_run.side_effect = subprocess.TimeoutExpired(
            cmd="fastfetch", timeout=COMMAND_TIMEOUT_SECONDS
        )

        from fetch_cord.tools import BashError, run_command

        with self.assertRaises(BashError):
            run_command(["fastfetch"])

    @patch("fetch_cord.tools.resources.path")
    def test_get_resource_path(self, mock_resources_path):
        """Test get_resource_path function."""
        mock_path = MagicMock()
        mock_path.__enter__ = MagicMock(return_value="/fake/path")
        mock_path.__exit__ = MagicMock(return_value=False)
        mock_resources_path.return_value = mock_path

        from fetch_cord.tools import get_resource_path

        result = get_resource_path("fetch_cord.resources", "test.yml")

        mock_resources_path.assert_called_once_with("fetch_cord.resources", "test.yml")
        self.assertEqual(result, "/fake/path")

    def test_bash_error_exception(self):
        """Test BashError exception can be raised."""
        from fetch_cord.tools import BashError

        with self.assertRaises(BashError):
            raise BashError("Test error")


class TestIntegration(unittest.TestCase):
    """Integration tests that verify module interactions."""

    def test_fetch_chain_fills_gaps(self):
        """The Fetch cache merges providers: earlier fields win, later fill gaps.

        Uses controlled fake providers rather than mocking the fastfetch binary,
        which is robust across Python versions and import ordering.
        """
        from fetch_cord.fetch import Fetch

        class FastfetchFake:
            name = "fastfetch"

            def fetch(self, skip=None):
                return {"os": "Debian GNU/Linux", "kernel": "6.8.0"}

        class CommandFake:
            name = "commands"

            def fetch(self, skip=None):
                return {"system_type": "Desktop"}

        fetch = Fetch([FastfetchFake(), CommandFake()])
        snap = fetch.snapshot()

        self.assertEqual(snap["os"], "Debian GNU/Linux")
        self.assertEqual(snap["kernel"], "6.8.0")
        self.assertEqual(snap["system_type"], "Desktop")


class TestFetchcordCmds(unittest.TestCase):
    """CommandProvider scripts in fetchcord_cmds.yml must be POSIX /bin/sh."""

    commands: dict[str, Any]

    @classmethod
    def setUpClass(cls) -> None:
        from fetch_cord.config import Config

        cls.commands = Config("fetchcord_cmds.yml")["commands"]

    def test_linux_motherboard_uses_explicit_dmi_paths(self) -> None:
        linux = self.commands["motherboard"]["Linux"]
        self.assertNotIn("board_{vendor,name}", linux)
        self.assertIn("/sys/devices/virtual/dmi/id/board_vendor", linux)
        self.assertIn("/sys/devices/virtual/dmi/id/board_name", linux)

    def test_mem_available_uses_fixed_precision(self) -> None:
        for script in (self.commands["mem"]["Linux"], self.commands["mem"]["Darwin"]):
            lines = [
                line.strip()
                for line in script.splitlines()
                if line.strip().startswith("AvailableMemory=$(awk")
            ]
            self.assertEqual(len(lines), 1, script)
            self.assertIn("printf", lines[0])
            self.assertIn("%.2f", lines[0])


if __name__ == "__main__":
    unittest.main(verbosity=2)
