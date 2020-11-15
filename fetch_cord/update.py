import urllib.request
import sys
import os


def update():
    print("Updating database...")
    url = "https://raw.githubusercontent.com/MrPotatoBobx/FetchCord/master/fetch_cord/ressources/infos.json"
    urllib.request.urlretrieve(
        url, os.path.dirname(__file__) + "/ressources/infos.json"
    )
    sys.exit(0)
