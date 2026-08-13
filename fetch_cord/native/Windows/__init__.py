import os

if os.name == "nt":
    from . import packages

    def fetch(component_class: str) -> str | None:
        fetch_map = {"packages": packages}

        if component_class not in fetch_map:
            return None

        return str(fetch_map[component_class].fetch())

else:

    def fetch(component_class: str) -> str | None:
        return None
