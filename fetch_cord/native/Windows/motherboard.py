"""Motherboard vendor and product, matching the Windows PowerShell command.

Joins BaseBoardManufacturer and BaseBoardProduct the same way Linux reports
board_vendor + board_name, so the host cycle's app_id/top_line can match
board-specific entries in motherboards.json (e.g. TUF) rather than only the
generic vendor.

e.g. "ASUSTeK COMPUTER INC. PRIME B760-PLUS D4"
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
    manufacturer = usable(registry.read(registry.BIOS, "BaseBoardManufacturer"))
    product = usable(registry.read(registry.BIOS, "BaseBoardProduct"))
    parts = [part for part in (manufacturer, product) if part]
    return " ".join(parts) or None
