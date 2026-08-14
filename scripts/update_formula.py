#!/usr/bin/env python3
"""Update the Homebrew formula to the latest FetchCord release.

The Homebrew tap (a repo named ``fetchcord/homebrew-fetchcord``) runs this
script from its own CI whenever a new FetchCord release is published, so the
formula's ``url``/``sha256`` always track the newest tag.

Usage (from the tap repo root, or with ``--formula``):
    python scripts/update_formula.py                # use the latest release
    python scripts/update_formula.py --tag v3.0.0   # pin a specific tag
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

REPO = "fetchcord/FetchCord"
# When run from the tap repo, the script is placed at <tap>/scripts/, so the
# formula resolves to <tap>/Formula/fetchcord.rb.
REPO_ROOT = Path(__file__).resolve().parent.parent
FORMULA = REPO_ROOT / "Formula" / "fetchcord.rb"


def tarball_url(tag: str) -> str:
    return f"https://github.com/{REPO}/archive/refs/tags/{tag}.tar.gz"


def latest_tag() -> str:
    url = f"https://api.github.com/repos/{REPO}/releases/latest"
    with urllib.request.urlopen(url) as resp:
        return str(json.load(resp)["tag_name"])


def sha256_of(tag: str) -> str:
    with urllib.request.urlopen(tarball_url(tag)) as resp:
        return hashlib.sha256(resp.read()).hexdigest()


def rewrite(text: str, tag: str, sha: str) -> str:
    """Replace the url/sha256 lines in a formula, leaving everything else."""
    url = tarball_url(tag)
    text = re.sub(r"^  url .*$", f'  url "{url}"', text, flags=re.MULTILINE)
    text = re.sub(r"^  sha256 .*$", f'  sha256 "{sha}"', text, flags=re.MULTILINE)
    return text


def update(tag: str | None = None) -> str:
    tag = tag or latest_tag()
    sha = sha256_of(tag)
    FORMULA.write_text(rewrite(FORMULA.read_text(), tag, sha))
    return f"Updated {FORMULA} to {tag} (sha256 {sha})"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tag", help="release tag (default: latest release)")
    args = parser.parse_args()
    try:
        print(update(args.tag))
    except (urllib.error.URLError, json.JSONDecodeError, KeyError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
