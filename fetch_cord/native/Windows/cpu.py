"""Processor name, matching Win32_Processor.Name.

e.g. "Intel(R) Core(TM) i7-9750H CPU @ 2.60GHz"
"""

from fetch_cord.native.Windows import registry


def fetch() -> str | None:
    name = registry.read(registry.CPU0, "ProcessorNameString")

    return name.strip() if name else None
