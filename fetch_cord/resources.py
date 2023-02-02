#from __future__ import annotations


try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources
import json

from .. import resources as fc_resources


def get_infos():
    with pkg_resources.open_text(fc_resources, "fetchcord_ids.json") as f:
        infos = json.load(f)

    return infos


def get_default_config():
    with pkg_resources.path(fc_resources, "default.conf") as path:
        return path

    return None
