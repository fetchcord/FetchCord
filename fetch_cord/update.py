#from __future__ import annotations

import urllib.request, sys, os
from ..args import parse_args

args = parse_args()

def update():
    print("Updating database...")
    url = f"https://raw.githubusercontent.com/MrPotatoBobx/FetchCord/{'testing' if args.testing else 'master'}/fetch_cord/resources/fetchcord_ids.json"
    urllib.request.urlretrieve(
        url, os.path.dirname(__file__) + "/resources/fetchcord_ids.json"
    )
    sys.exit(0)
