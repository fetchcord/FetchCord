import os

if os.name == "nt":
    from typing import Optional
    from . import packages

    def fetch(component_class: str) -> Optional[str]:
        fetch_map = {"packages": packages}

        if component_class not in fetch_map:
            return None

        return fetch_map[component_class].fetch()

else:

    def fetch(component_class: str) -> None:
        return "Not implemented for this platform."
