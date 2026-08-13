import platform
from typing import cast

from fetch_cord.native import Windows

fetch_map = {"Windows": Windows}


def fetch(component_class: str) -> str | None:
    sys_platform = platform.system()

    if sys_platform not in fetch_map:
        return None

    return cast(str | None, fetch_map[sys_platform].fetch(component_class))
