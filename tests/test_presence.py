"""Tests for the presence-payload builder and the Cycle -> rpc.update mapping.

These verify that the system info gathered by hardware detection is turned into
the exact Discord Rich Presence payload — no Discord connection required.
"""

import unittest
from threading import Event
from unittest.mock import MagicMock, patch

from fetch_cord.constants import UNKNOWN_COMPONENT_ID
from fetch_cord.presence import build_presence_activity, parse_buttons


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


class TestParseButtons(unittest.TestCase):
    """A typo in the config must cost a button, never the whole presence."""

    GOOD = {"label": "Dotfiles", "url": "https://github.com/me/dotfiles"}

    def test_accepts_a_valid_button(self) -> None:
        self.assertEqual(parse_buttons([self.GOOD]), [self.GOOD])

    def test_nothing_configured_is_an_empty_list(self) -> None:
        self.assertEqual(parse_buttons(None), [])
        self.assertEqual(parse_buttons([]), [])

    def test_strips_surrounding_whitespace(self) -> None:
        parsed = parse_buttons(
            [{"label": "  Dotfiles  ", "url": "  https://example.com  "}]
        )

        self.assertEqual(parsed, [{"label": "Dotfiles", "url": "https://example.com"}])

    @patch("builtins.print")
    def test_rejects_http_urls(self, mock_print: MagicMock) -> None:
        """Discord only accepts https on presence buttons."""
        self.assertEqual(
            parse_buttons([{"label": "Site", "url": "http://example.com"}]), []
        )

    @patch("builtins.print")
    def test_rejects_a_half_filled_button(self, mock_print: MagicMock) -> None:
        self.assertEqual(parse_buttons([{"label": "Site"}]), [])
        self.assertEqual(parse_buttons([{"url": "https://example.com"}]), [])

    @patch("builtins.print")
    def test_rejects_an_over_long_label(self, mock_print: MagicMock) -> None:
        self.assertEqual(
            parse_buttons([{"label": "x" * 33, "url": "https://example.com"}]), []
        )
        self.assertEqual(
            len(parse_buttons([{"label": "x" * 32, "url": "https://example.com"}])), 1
        )

    @patch("builtins.print")
    def test_keeps_the_good_button_when_another_is_bad(
        self, mock_print: MagicMock
    ) -> None:
        parsed = parse_buttons([{"label": "Bad", "url": "ftp://nope"}, self.GOOD])

        self.assertEqual(parsed, [self.GOOD])

    @patch("builtins.print")
    def test_caps_at_the_discord_limit(self, mock_print: MagicMock) -> None:
        parsed = parse_buttons(
            [{"label": f"b{n}", "url": "https://example.com"} for n in range(5)]
        )

        self.assertEqual(len(parsed), 2)

    @patch("builtins.print")
    def test_survives_a_malformed_config(self, mock_print: MagicMock) -> None:
        self.assertEqual(parse_buttons("not a list"), [])
        self.assertEqual(parse_buttons(["not a mapping"]), [])
        self.assertEqual(parse_buttons([None]), [])


class TestButtonsInThePayload(unittest.TestCase):
    def test_buttons_are_omitted_when_not_configured(self) -> None:
        """pypresence rejects an empty buttons list, so don't send the key."""
        payload = build_presence_activity(
            details="d",
            state="s",
            large_image="big",
            large_text="l",
            small_image="i",
            small_text="t",
            start=1,
        )

        self.assertNotIn("buttons", payload)

    def test_buttons_are_included_when_configured(self) -> None:
        buttons = [{"label": "Dotfiles", "url": "https://example.com"}]
        payload = build_presence_activity(
            details="d",
            state="s",
            large_image="big",
            large_text="l",
            small_image="i",
            small_text="t",
            start=1,
            buttons=buttons,
        )

        self.assertEqual(payload["buttons"], buttons)

    def test_buttons_survive_an_unresolved_small_icon(self) -> None:
        """Dropping the icon pair must not take the buttons with it."""
        buttons = [{"label": "Dotfiles", "url": "https://example.com"}]
        payload = build_presence_activity(
            details="d",
            state="s",
            large_image="big",
            large_text="l",
            small_image=UNKNOWN_COMPONENT_ID,
            small_text="t",
            start=1,
            buttons=buttons,
        )

        self.assertIsNone(payload["small_image"])
        self.assertIsNone(payload["small_text"])
        self.assertEqual(payload["buttons"], buttons)


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
