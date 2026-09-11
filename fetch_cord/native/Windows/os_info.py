"""Windows edition name, matching Win32_OperatingSystem.Caption.

The registry's ProductName still reads "Windows 10 Pro" on Windows 11, so the
build number decides the release and the name is corrected to match what WMI
would report.
"""

from fetch_cord.native.Windows import registry

# Windows 11 starts here; the registry name was never updated for it.
WINDOWS_11_BUILD = 22000


def fetch() -> str | None:
    product = registry.read(registry.CURRENT_VERSION, "ProductName")
    if product is None:
        return None

    build = registry.read_int(registry.CURRENT_VERSION, "CurrentBuildNumber")
    if build is not None and build >= WINDOWS_11_BUILD:
        product = product.replace("Windows 10", "Windows 11")

    # WMI's Caption is prefixed; match it so the value is interchangeable with
    # the PowerShell command this replaces.
    if not product.startswith("Microsoft "):
        product = f"Microsoft {product}"

    return product
