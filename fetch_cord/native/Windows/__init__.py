from typing import Optional
from . import packages

fetch_map = {"packages": packages}


def fetch(component_class: str) -> Optional[str | None]:

    if component_class not in fetch_map:
        return None

    return fetch_map[component_class].fetch()
