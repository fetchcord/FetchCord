"""Tests for the --report-hardware markdown report.

The report exists so an "unknown motherboard" issue arrives with the raw
string needed to write an id-table pattern, so these pin down that the raw
string is present and that a miss is called a miss.
"""

import unittest
from unittest.mock import MagicMock, patch

from fetch_cord.report import build, report

IDS: dict[str, dict[str, list[str]]] = {
    "os": {"os-id": ["(?i)debian"], "os-generic": ["unknown"]},
    "cpu": {"cpu-id": ["(?i)ryzen"], "cpu-generic": ["unknown"]},
    "gpu": {"gpu-id": ["(?i)nvidia"]},
    "motherboard": {"mb-id": ["(?i)asus"]},
    "terminal": {"term-id": ["(?i)xterm"]},
    "shell": {"shell-id": ["(?i)bash"]},
    "system_type": {"desktop": ["(?i)desktop"]},
}

SNAPSHOT = {
    "os": "Debian GNU/Linux",
    "cpu": "AMD Ryzen 7 5800X",
    "gpu": "NVIDIA GeForce RTX 3080",
    "motherboard": "ASUSTeK COMPUTER INC.",
    "terminal": "xterm",
    "shell": "bash",
    "system_type": "Desktop",
}


class TestBuild(unittest.TestCase):
    def test_everything_matching_reports_no_missing(self) -> None:
        text, missing = build(SNAPSHOT, IDS)

        self.assertEqual(missing, 0)
        self.assertIn("Everything on this machine matched", text)
        self.assertNotIn("needs an entry", text)

    def test_a_miss_is_counted_and_flagged(self) -> None:
        snapshot = {**SNAPSHOT, "motherboard": "Some Unlisted Board Co."}

        text, missing = build(snapshot, IDS)

        self.assertEqual(missing, 1)
        self.assertIn("needs an entry", text)
        self.assertIn("1 component(s) found no match", text)

    def test_the_raw_detected_string_is_in_the_table(self) -> None:
        """That string is the whole point - it's what a pattern must match."""
        snapshot = {**SNAPSHOT, "motherboard": "Micro-Star International Co., Ltd."}

        text, _ = build(snapshot, IDS)

        self.assertIn("Micro-Star International Co., Ltd.", text)

    def test_a_missing_field_is_not_counted_as_a_miss(self) -> None:
        """Absent hardware needs no id-table entry, so it isn't a miss."""
        snapshot = {key: value for key, value in SNAPSHOT.items() if key != "gpu"}

        text, missing = build(snapshot, IDS)

        self.assertEqual(missing, 0)
        self.assertIn("not detected on this machine", text)

    def test_the_not_found_sentinel_counts_as_absent(self) -> None:
        snapshot = {**SNAPSHOT, "system_type": "Not Found"}

        text, missing = build(snapshot, IDS)

        self.assertEqual(missing, 0)
        self.assertIn("not detected on this machine", text)

    def test_every_component_gets_a_row(self) -> None:
        """A silently dropped row is exactly what this command must not do."""
        text, _ = build(SNAPSHOT, IDS)

        for title in (
            "OS",
            "CPU",
            "GPU",
            "Motherboard",
            "Terminal",
            "Shell",
            "System type",
        ):
            with self.subTest(component=title):
                self.assertIn(f"| {title} |", text)

    def test_a_missing_id_table_is_reported_not_skipped(self) -> None:
        ids = {key: value for key, value in IDS.items() if key != "gpu"}

        text, _ = build(SNAPSHOT, ids)

        self.assertIn("| GPU |", text)
        self.assertIn("no id table loaded", text)

    def test_os_and_cpu_are_matched_lowercased(self) -> None:
        """Mirrors the main loop, which lowercases before looking these up."""
        ids = {**IDS, "os": {"os-id": ["^debian gnu"]}}

        _, missing = build({**SNAPSHOT, "os": "Debian GNU/Linux"}, ids)

        self.assertEqual(missing, 0)

    def test_output_is_pasteable_markdown(self) -> None:
        text, _ = build(SNAPSHOT, IDS)

        self.assertTrue(text.startswith("<!-- Paste this into a FetchCord issue -->"))
        self.assertIn("| Component | Detected | Matched id | Status |", text)
        self.assertIn("| --- | --- | --- | --- |", text)


class TestReport(unittest.TestCase):
    @patch("builtins.print")
    def test_report_prints_and_succeeds(self, mock_print: MagicMock) -> None:
        self.assertEqual(report(SNAPSHOT, IDS), 0)
        mock_print.assert_called_once()

    @patch("builtins.print")
    def test_report_succeeds_even_with_misses(self, mock_print: MagicMock) -> None:
        """The report ran fine; unmatched hardware isn't a failure of it."""
        snapshot = {**SNAPSHOT, "motherboard": "Unlisted"}

        self.assertEqual(report(snapshot, IDS), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
