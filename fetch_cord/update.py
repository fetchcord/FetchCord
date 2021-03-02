#from __future__ import annotations

import urllib.request, sys, os


def update():
    print("Updating database...")
    url = "https://raw.githubusercontent.com/MrPotatoBobx/FetchCord/master/fetch_cord/resources/fetchcord_ids.json"
    urllib.request.urlretrieve(
        url, os.path.dirname(__file__) + "/resources/fetchcord_ids.json"
    )
    sys.exit(0)
