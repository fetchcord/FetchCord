# from __future__ import annotations


try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources

from fetch_cord import resources as fc_resources


def get_default_config() -> str:
    with pkg_resources.path(fc_resources, "default.conf") as path:
        return path
