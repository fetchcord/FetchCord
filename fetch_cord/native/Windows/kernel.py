"""Windows version string, matching Win32_OperatingSystem.Version.

e.g. "10.0.26100"
"""

from fetch_cord.native.Windows import registry


def fetch() -> str | None:
    build = registry.read(registry.CURRENT_VERSION, "CurrentBuildNumber")
    if build is None:
        return None

    major = registry.read_int(registry.CURRENT_VERSION, "CurrentMajorVersionNumber")
    minor = registry.read_int(registry.CURRENT_VERSION, "CurrentMinorVersionNumber")

    # Present since Windows 10; fall back to the values every release carries.
    if major is None:
        major = 10
    if minor is None:
        minor = 0

    return f"{major}.{minor}.{build}"
