import os
from types import ModuleType

if os.name == "nt":
    from . import cpu, host, kernel, mem, motherboard, os_info, packages

    fetch_map: dict[str, ModuleType] = {
        "cpu": cpu,
        "host": host,
        "kernel": kernel,
        "mem": mem,
        "motherboard": motherboard,
        "os": os_info,
        "packages": packages,
    }

    def fetch(component_class: str) -> str | None:
        module = fetch_map.get(component_class)
        if module is None:
            return None

        # A fetcher returns None when the value is not readable on this
        # machine; pass that through rather than stringifying it, so the next
        # provider fills the gap instead of showing "None".
        value = module.fetch()

        return str(value) if value else None

else:

    def fetch(component_class: str) -> str | None:
        return None
