"""Motherboard manufacturer, matching Win32_BaseBoard.Manufacturer.

e.g. "ASUSTeK COMPUTER INC."
"""

from fetch_cord.native.Windows import registry

# Strings firmware ships when the vendor never filled the field in. Returning
# None for these lets another provider supply something better.
PLACEHOLDERS = {
    "",
    "to be filled by o.e.m.",
    "default string",
    "system manufacturer",
    "not applicable",
    "not specified",
    "none",
    "o.e.m.",
    "unknown",
}


def usable(value: str | None) -> str | None:
    """The value, unless it is firmware boilerplate."""
    if value is None:
        return None

    value = value.strip()

    return None if value.lower() in PLACEHOLDERS else value


def fetch() -> str | None:
    return usable(registry.read(registry.BIOS, "BaseBoardManufacturer"))
