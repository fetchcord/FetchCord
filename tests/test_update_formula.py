"""Tests for the Homebrew formula updater used by the tap's release workflow."""

import unittest

from scripts.update_formula import rewrite, tarball_url


class TestRewrite(unittest.TestCase):
    def test_updates_url_and_sha256(self) -> None:
        text = (
            '  url "https://github.com/fetchcord/FetchCord/archive/refs/tags/v3.0.0.tar.gz"\n'
            '  sha256 "REPLACE_WITH_RELEASE_TARBALL_SHA256"\n'
            '  license "MIT"\n'
        )
        out = rewrite(text, "v3.1.0", "abc123")
        self.assertIn(
            'url "https://github.com/fetchcord/FetchCord/archive/refs/tags/v3.1.0.tar.gz"',
            out,
        )
        self.assertIn('sha256 "abc123"', out)
        self.assertIn('license "MIT"', out)  # untouched lines preserved

    def test_is_idempotent(self) -> None:
        text = '  url "x"\n  sha256 "y"\n'
        once = rewrite(text, "v3.2.0", "s1")
        twice = rewrite(once, "v3.2.0", "s1")
        self.assertEqual(once, twice)

    def test_only_matches_indented_lines(self) -> None:
        # A top-level (non-indented) url line must not be clobbered.
        text = '#   url "not the formula url"\n  url "old"\n'
        out = rewrite(text, "v3.0.0", "sha")
        self.assertIn('#   url "not the formula url"', out)
        self.assertIn(
            'url "https://github.com/fetchcord/FetchCord/archive/refs/tags/v3.0.0.tar.gz"',
            out,
        )

    def test_preserves_livecheck_block(self) -> None:
        # The livecheck block's 4-space url line must survive a rewrite.
        text = (
            '  url "old"\n'
            '  sha256 "oldsha"\n'
            "  livecheck do\n"
            '    url "https://github.com/fetchcord/FetchCord/releases"\n'
            "    strategy :github_latest\n"
            "  end\n"
        )
        out = rewrite(text, "v3.0.0", "newsha")
        self.assertIn(
            'url "https://github.com/fetchcord/FetchCord/archive/refs/tags/v3.0.0.tar.gz"',
            out,
        )
        self.assertIn('  sha256 "newsha"', out)
        self.assertIn('    url "https://github.com/fetchcord/FetchCord/releases"', out)
        self.assertIn("strategy :github_latest", out)


class TestTarballUrl(unittest.TestCase):
    def test_builds_github_tarball_url(self) -> None:
        self.assertEqual(
            tarball_url("v3.0.0"),
            "https://github.com/fetchcord/FetchCord/archive/refs/tags/v3.0.0.tar.gz",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
