import json

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources
import fetch_cord.ressources as ressources

def get_infos():
    with pkg_resources.open_text(ressources, 'fetchcord_ids.json') as f:
        infos = json.load(f)

    return infos