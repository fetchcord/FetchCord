"""Tests for the presence-payload builder and the Cycle -> rpc.update mapping.

These verify that the system info gathered by hardware detection is turned into
the exact Discord Rich Presence payload — no Discord connection required.
"""

import unittest
from threading import Event
from unittest.mock import MagicMock, patch

from fetch_cord.presence import build_presence_activity


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

    def test_drops_small_pair_when_icon_is_unresolved(self) -> None:
        """No icon means no tooltip - Discord has nothing to attach it to.

        get_component_id falls back to the literal "unknown" when a component
        isn't in the id table, and that isn't an uploaded asset. system_types
        and desktop have no "unknown" entry at all, so any machine whose
        system_type doesn't resolve (a desktop with no battery, say) hit this
        on both the os and host cycles.
        """
        for placeholder in ("unknown", "Not Found", ""):
            with self.subTest(small_image=placeholder):
                payload = build_presence_activity(
                    details="6.8.0",
                    state="432 packages",
                    large_image="big",
                    large_text="Debian GNU/Linux",
                    small_image=placeholder,
                    small_text="Not Found",
                    start=1700000000,
                )
                self.assertIsNone(payload["small_image"])
                self.assertIsNone(payload["small_text"])
                # The rest of the payload is untouched.
                self.assertEqual(payload["details"], "6.8.0")
                self.assertEqual(payload["large_text"], "Debian GNU/Linux")

    def test_keeps_icon_but_drops_placeholder_tooltip(self) -> None:
        payload = build_presence_activity(
            details="6.8.0",
            state="432 packages",
            large_image="big",
            large_text="Debian GNU/Linux",
            small_image="desktop",
            small_text="Not Found",
            start=1700000000,
        )
        self.assertEqual(payload["small_image"], "desktop")
        self.assertIsNone(payload["small_text"])

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
