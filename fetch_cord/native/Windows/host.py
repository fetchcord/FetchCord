"""Motherboard product name, matching Win32_BaseBoard.Product.

e.g. "PRIME B760-PLUS D4"
"""

from fetch_cord.native.Windows import motherboard, registry


def fetch() -> str | None:
    return motherboard.usable(registry.read(registry.BIOS, "BaseBoardProduct"))
