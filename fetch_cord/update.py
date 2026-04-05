# from __future__ import annotations

import os
import sys
import urllib.request

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


def update():
    print("Updating database...")
    branch = "testing" if args.testing else "master"
    base_url = f"https://raw.githubusercontent.com/fetchcord/FetchCord/{branch}/fetch_cord/resources/"
    resources_dir = os.path.dirname(__file__) + "/resources/"

    for filename in RESOURCE_FILES:
        url = base_url + filename
        filepath = resources_dir + filename
        try:
            urllib.request.urlretrieve(url, filepath)
            print(f"  Updated {filename}")
        except Exception as e:
            print(f"  Failed to update {filename}: {e}")

    print("Update complete!")
    sys.exit(0)
