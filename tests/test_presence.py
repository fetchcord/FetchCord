"""Tests for the presence-payload builder and the Cycle -> rpc.update mapping.

These verify that the system info gathered by hardware detection is turned into
the exact Discord Rich Presence payload — no Discord connection required.
"""

import unittest
from threading import Event
from unittest.mock import MagicMock, patch

from fetch_cord.presence import ResolvedCycle, build_presence_activity, resolve_cycle


class TestBuildPresenceActivity(unittest.TestCase):
    def test_returns_expected_payload(self) -> None:
        payload = build_presence_activity(
            details="6.8.0",
            state="432 packages",
            large_image="big",
            large_text="Debian GNU/Linux",
            small_image="desktop",
            small_text="Desktop",
            start=1700000000,
        )
        self.assertEqual(
            payload,
            {
                "details": "6.8.0",
                "state": "432 packages",
                "large_image": "big",
                "large_text": "Debian GNU/Linux",
                "small_image": "desktop",
                "small_text": "Desktop",
                "start": 1700000000,
            },
        )

    def test_accepts_not_found_sentinel(self) -> None:
        payload = build_presence_activity(
            details="Not Found",
            state="Not Found",
            large_image="big",
            large_text="Not Found",
            small_image="Not Found",
            small_text="Not Found",
            start=0,
        )
        self.assertEqual(payload["details"], "Not Found")
        self.assertEqual(payload["state"], "Not Found")

    def test_is_pure(self) -> None:
        """Calling it twice yields equal but independent dicts."""
        a = build_presence_activity(
            details="x",
            state="y",
            large_image="big",
            large_text="x",
            small_image="i",
            small_text="s",
            start=1,
        )
        b = build_presence_activity(
            details="x",
            state="y",
            large_image="big",
            large_text="x",
            small_image="i",
            small_text="s",
            start=1,
        )
        self.assertEqual(a, b)
        a["details"] = "changed"
        self.assertNotEqual(a, b)


class TestResolveCycle(unittest.TestCase):
    """One resolver feeds the presence loop, --dry-run and validate.py."""

    IDS = {
        "os": {"os-id": ["(?i)debian"]},
        "system_type": {"desktop": ["(?i)desktop"]},
        "cpu": {"apple-id": ["(?i)apple"]},
    }

    SNAPSHOT = {
        "os": "Debian GNU/Linux",
        "kernel": "6.8.0",
        "packages": "432 packages",
        "system_type": "Desktop",
    }

    def _resolve(self, **overrides: str) -> ResolvedCycle:
        kwargs: dict[str, str] = {
            "name": "os",
            "app_id": "os",
            "top_line": "kernel",
            "bottom_line": "packages",
            "small_icon": "system_type",
        }
        kwargs.update(overrides)
        return resolve_cycle(self.SNAPSHOT, self.IDS, **kwargs)

    def test_maps_snapshot_fields_onto_the_cycle(self) -> None:
        resolved = self._resolve()

        self.assertEqual(resolved.name, "os")
        self.assertEqual(resolved.client_id, "os-id")
        self.assertEqual(resolved.app, "Debian GNU/Linux")
        self.assertEqual(resolved.top, "6.8.0")
        self.assertEqual(resolved.bottom, "432 packages")
        self.assertEqual(resolved.icon, "Desktop")
        self.assertEqual(resolved.icon_id, "desktop")
        self.assertEqual(resolved.large_image, "big")

    @patch("builtins.print")
    def test_missing_fields_become_the_sentinel(self, _print: MagicMock) -> None:
        resolved = self._resolve(top_line="nope", bottom_line="also-nope")

        self.assertEqual(resolved.top, "Not Found")
        self.assertEqual(resolved.bottom, "Not Found")

    def test_apple_silicon_gets_a_per_chip_large_image(self) -> None:
        resolved = resolve_cycle(
            {"cpu": "Apple M4 Pro"},
            {"cpu": {"apple-id": ["(?i)apple"]}},
            name="hardware",
            app_id="cpu",
            top_line="cpu",
            bottom_line="cpu",
            small_icon="cpu",
        )

        self.assertEqual(resolved.large_image, "apple-m4-pro")

    def test_activity_matches_the_payload_builder(self) -> None:
        resolved = self._resolve()

        self.assertEqual(
            resolved.activity(1700000000),
            build_presence_activity(
                details="6.8.0",
                state="432 packages",
                large_image="big",
                large_text="Debian GNU/Linux",
                small_image="desktop",
                small_text="Desktop",
                start=1700000000,
            ),
        )


class TestCycleUpdatePayload(unittest.TestCase):
    """Cycle.update must hand the mapped values to pypresence as an activity."""

    @patch("fetch_cord.cycle.psutil.boot_time", return_value=1700000000)
    def test_update_sends_activity_to_rpc(self, mock_boot: MagicMock) -> None:
        from fetch_cord.cycle import Cycle

        cycle = Cycle({"name": "t", "time": 30}, Event())
        mock_rpc = MagicMock()
        cycle.rpc = mock_rpc
        cycle.wait = MagicMock()

        cycle.update(
            app="Debian GNU/Linux",
            bottom="432 packages",
            top="6.8.0",
            icon="Desktop",
            icon_id="desktop",
        )

        mock_rpc.update.assert_called_once_with(
            details="6.8.0",
            state="432 packages",
            large_image="big",
            large_text="Debian GNU/Linux",
            small_image="desktop",
            small_text="Desktop",
            start=1700000000,
        )
        cycle.wait.assert_called_once_with(30)

    @patch("fetch_cord.cycle.psutil.boot_time", return_value=1700000000)
    def test_update_uses_apple_m_large_image(self, mock_boot: MagicMock) -> None:
        from fetch_cord.cycle import Cycle

        cycle = Cycle({"name": "t", "time": 30}, Event())
        mock_rpc = MagicMock()
        cycle.rpc = mock_rpc
        cycle.wait = MagicMock()

        cycle.update(
            app="macOS 15.1",
            bottom="0 packages",
            top="24.3.0",
            icon="Apple M4 Pro",
            icon_id="apple-m4-pro",
            large_image="apple-m4-pro",
        )

        mock_rpc.update.assert_called_once_with(
            details="24.3.0",
            state="0 packages",
            large_image="apple-m4-pro",
            large_text="macOS 15.1",
            small_image="apple-m4-pro",
            small_text="Apple M4 Pro",
            start=1700000000,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
