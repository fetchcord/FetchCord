# from __future__ import annotations

import os
import sys
import urllib.request
from pathlib import Path

from fetch_cord.args import parse_args

args = parse_args()

RESOURCE_FILES = [
    "cpus.json",
    "gpus.json",
    "os.json",
    "terminal.json",
    "shell.json",
    "motherboards.json",
    "system_types.json",
]


def validate_filename(filename: str) -> bool:
    """Validate filename to prevent path traversal attacks."""
    if not filename:
        return False
    if ".." in filename or "/" in filename or "\\" in filename:
        return False
    allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_.")
    if not all(c in allowed_chars for c in filename):
        return False
    if not filename.endswith(".json"):
        return False
    return True


def get_resources_dir() -> Path:
    """Get the resources directory path."""
    return Path(__file__).parent / "resources"


def update():
    print("Updating database...")
    branch = "testing" if args.testing else "master"
    base_url = f"https://raw.githubusercontent.com/fetchcord/FetchCord/{branch}/fetch_cord/resources/"
    resources_dir = get_resources_dir()

    # Ensure resources directory exists
    try:
        resources_dir.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        print(f"Error: Cannot create resources directory: {e}")
        sys.exit(1)

    updated = 0
    failed = 0

    for filename in RESOURCE_FILES:
        if not validate_filename(filename):
            print(f"  Skipping invalid filename: {filename}")
            failed += 1
            continue

        url = base_url + filename
        filepath = resources_dir / filename

        try:
            urllib.request.urlretrieve(url, str(filepath))
            print(f"  Updated {filename}")
            updated += 1
        except Exception as e:
            print(f"  Failed to update {filename}: {e}")
            failed += 1

    print(f"Update complete! Updated: {updated}, Failed: {failed}")
    sys.exit(0 if failed == 0 else 1)
