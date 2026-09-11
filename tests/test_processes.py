"""Tests for pausing the presence while another program owns the status.

Discord shows one activity at a time, so these cover the decision about when
FetchCord should get out of the way - no real process scanning required.
"""

import unittest
from unittest.mock import MagicMock, patch

import psutil

from fetch_cord.processes import PauseWatcher, find_running, running_names


def fake_processes(*names: str) -> list[MagicMock]:
    return [MagicMock(info={"name": name}) for name in names]


class TestRunningNames(unittest.TestCase):
    @patch("fetch_cord.processes.psutil.process_iter")
    def test_lowercases_every_name(self, mock_iter: MagicMock) -> None:
        mock_iter.return_value = fake_processes("Steam.exe", "Discord")

        self.assertEqual(running_names(), ["steam.exe", "discord"])

    @patch("fetch_cord.processes.psutil.process_iter")
    def test_skips_processes_without_a_name(self, mock_iter: MagicMock) -> None:
        mock_iter.return_value = fake_processes("steam", "") + [
            MagicMock(info={"name": None})
        ]

        self.assertEqual(running_names(), ["steam"])

    @patch("fetch_cord.processes.psutil.process_iter")
    def test_a_process_exiting_mid_scan_does_not_abandon_it(
        self, mock_iter: MagicMock
    ) -> None:
        """Processes come and go while we iterate; that's normal, not fatal."""
        dying = MagicMock()
        type(dying).info = property(
            lambda self: (_ for _ in ()).throw(psutil.NoSuchProcess(1))
        )
        mock_iter.return_value = [dying, *fake_processes("spotify")]

        self.assertEqual(running_names(), ["spotify"])

    @patch(
        "fetch_cord.processes.psutil.process_iter", side_effect=psutil.AccessDenied()
    )
    def test_returns_empty_when_the_scan_is_refused(self, mock_iter: MagicMock) -> None:
        self.assertEqual(running_names(), [])


class TestFindRunning(unittest.TestCase):
    @patch("fetch_cord.processes.running_names")
    def test_matches_with_or_without_the_exe_suffix(
        self, mock_names: MagicMock
    ) -> None:
        """One config line has to work on Windows and on Linux."""
        mock_names.return_value = ["steam.exe"]
        self.assertEqual(find_running(["steam"]), "steam")

        mock_names.return_value = ["steam"]
        self.assertEqual(find_running(["steam.exe"]), "steam.exe")

    @patch("fetch_cord.processes.running_names", return_value=["discord", "spotify"])
    def test_returns_the_name_as_written(self, mock_names: MagicMock) -> None:
        self.assertEqual(find_running(["Steam", "SPOTIFY"]), "SPOTIFY")

    @patch("fetch_cord.processes.running_names", return_value=["discord"])
    def test_returns_none_when_nothing_matches(self, mock_names: MagicMock) -> None:
        self.assertIsNone(find_running(["steam", "spotify"]))

    @patch("fetch_cord.processes.running_names")
    def test_empty_config_never_scans(self, mock_names: MagicMock) -> None:
        self.assertIsNone(find_running([]))
        self.assertIsNone(find_running(["", "  "]))
        mock_names.assert_not_called()

    @patch("fetch_cord.processes.running_names", return_value=["steam.exe"])
    def test_substrings_do_not_match(self, mock_names: MagicMock) -> None:
        """ "steam" must not be matched by "steamwebhelper"."""
        self.assertIsNone(find_running(["team"]))


class TestPauseWatcher(unittest.TestCase):
    @patch("fetch_cord.processes.running_names", return_value=["steam.exe"])
    @patch("builtins.print")
    def test_announces_start_and_stop_once_each(
        self, mock_print: MagicMock, mock_names: MagicMock
    ) -> None:
        """Checked every cycle, so a line per check would be noise."""
        watcher = PauseWatcher(["steam"])

        self.assertEqual(watcher.check(), "steam")
        self.assertEqual(watcher.check(), "steam")

        mock_names.return_value = []
        self.assertIsNone(watcher.check())
        self.assertIsNone(watcher.check())

        printed = [str(call) for call in mock_print.call_args_list]
        self.assertEqual(len([p for p in printed if "Pausing" in p]), 1)
        self.assertEqual(len([p for p in printed if "resuming" in p]), 1)

    @patch("fetch_cord.processes.running_names")
    def test_no_names_configured_is_a_no_op(self, mock_names: MagicMock) -> None:
        watcher = PauseWatcher([])

        self.assertIsNone(watcher.check())
        mock_names.assert_not_called()

    def test_blank_entries_are_dropped(self) -> None:
        self.assertEqual(PauseWatcher(["steam", "", "  "]).names, ["steam"])

    def test_none_is_accepted(self) -> None:
        self.assertEqual(PauseWatcher(None).names, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
