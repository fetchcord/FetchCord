import urllib.request
import sys
import os


def update():
    print("Updating database...")
    url = "https://raw.githubusercontent.com/MrPotatoBobx/FetchCord/master/fetch_cord/testing.py"
    urllib.request.urlretrieve(url, os.path.dirname(__file__) + "/testing.py")
    sys.exit(0)



