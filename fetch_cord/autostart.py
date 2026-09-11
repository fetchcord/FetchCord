"""Optional "start FetchCord when I sign in" support, on every platform.

Each platform gets the mechanism its users expect - a per-user Run key on
Windows, a LaunchAgent on macOS, a systemd user service on Linux - behind one
pair of flags. None of them needs administrator rights, and none touches
anything outside the current user's own configuration.
"""

import os
import platform
import shutil
import sys

from fetch_cord.tools import BashError, exec_bash

RUN_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"
VALUE_NAME = "FetchCord"

AGENT_LABEL = "org.fetchcord.fetchcord"
AGENT_NAME = AGENT_LABEL + ".plist"

SERVICE_NAME = "fetchcord.service"
SERVICE_UNIT = """[Unit]
Description=FetchCord - system info as Discord Rich Presence
After=graphical-session.target

[Service]
Type=simple
ExecStart={command}
Restart=on-failure
RestartSec=30

[Install]
WantedBy=default.target
"""

AGENT_PLIST = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>{label}</string>
    <key>ProgramArguments</key>
    <array>
{arguments}
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <false/>
</dict>
</plist>
"""


class UnsupportedPlatformError(RuntimeError):
    """Raised when autostart isn't available on this platform."""


def launcher() -> list[str]:
    """The command that starts FetchCord, as argv.

    Prefers the installed console script, falling back to running the module
    with the interpreter we're on now - which is what a pipx or venv install
    needs.
    """
    if platform.system() == "Windows":
        # The windowless launcher keeps a console from flashing up at sign-in.
        found = shutil.which("fetchcordw") or shutil.which("fetchcord")
        if found:
            return [found]

        executable = sys.executable
        windowless = os.path.join(os.path.dirname(executable), "pythonw.exe")
        if os.path.exists(windowless):
            executable = windowless
        return [executable, "-m", "fetch_cord"]

    found = shutil.which("fetchcord")
    if found:
        return [found]
    return [sys.executable, "-m", "fetch_cord"]


def _quote(argv: list[str]) -> str:
    return " ".join(f'"{arg}"' if " " in arg else arg for arg in argv)


# -- Windows ---------------------------------------------------------------


def _windows_status() -> str | None:
    import winreg

    try:
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, RUN_KEY, 0, winreg.KEY_READ
        ) as key:
            value, _ = winreg.QueryValueEx(key, VALUE_NAME)
    except OSError:
        return None
    return str(value)


def _windows_install() -> str:
    import winreg

    command = _quote(launcher())
    with winreg.CreateKeyEx(
        winreg.HKEY_CURRENT_USER, RUN_KEY, 0, winreg.KEY_SET_VALUE
    ) as key:
        winreg.SetValueEx(key, VALUE_NAME, 0, winreg.REG_SZ, command)
    return command


def _windows_uninstall() -> bool:
    import winreg

    try:
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, RUN_KEY, 0, winreg.KEY_SET_VALUE
        ) as key:
            winreg.DeleteValue(key, VALUE_NAME)
    except OSError:
        return False
    return True


# -- macOS -----------------------------------------------------------------


def agent_path() -> str:
    return os.path.expanduser(os.path.join("~/Library/LaunchAgents", AGENT_NAME))


def _macos_status() -> str | None:
    path = agent_path()
    return path if os.path.exists(path) else None


def _macos_install() -> str:
    path = agent_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)

    arguments = "\n".join(f"        <string>{arg}</string>" for arg in launcher())
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(AGENT_PLIST.format(label=AGENT_LABEL, arguments=arguments))

    # Best effort: the plist alone is enough from the next login onwards.
    _try_bash(f'launchctl load "{path}"')
    return path


def _macos_uninstall() -> bool:
    path = agent_path()
    if not os.path.exists(path):
        return False

    _try_bash(f'launchctl unload "{path}"')
    os.remove(path)
    return True


# -- Linux -----------------------------------------------------------------


def unit_path() -> str:
    # Same location the existing --install flag uses, so the two don't end up
    # managing two different copies of the unit.
    home = os.path.expanduser("~")
    return os.path.join(home, ".local", "share", "systemd", "user", SERVICE_NAME)


def _linux_status() -> str | None:
    path = unit_path()
    return path if os.path.exists(path) else None


def _linux_install() -> str:
    path = unit_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w", encoding="utf-8") as handle:
        handle.write(SERVICE_UNIT.format(command=_quote(launcher())))

    _try_bash("systemctl --user daemon-reload")
    _try_bash(f'systemctl --user enable --now "{path}"')
    return path


def _linux_uninstall() -> bool:
    path = unit_path()
    if not os.path.exists(path):
        return False

    _try_bash(f'systemctl --user disable --now "{path}"')
    os.remove(path)
    _try_bash("systemctl --user daemon-reload")
    return True


def _try_bash(command: str) -> bool:
    """Run a command, treating failure as non-fatal.

    A machine without systemd or launchctl still gets a valid unit/plist
    written, which is the part that matters at next login.
    """
    try:
        exec_bash(command)
    except (BashError, OSError):
        return False
    return True


# -- dispatch --------------------------------------------------------------

SUPPORTED = ("Windows", "Darwin", "Linux")


def _check_supported() -> str:
    system = platform.system()
    if system not in SUPPORTED:
        raise UnsupportedPlatformError(f"Autostart is not supported on {system}.")
    return system


def status() -> str | None:
    """Where autostart is configured, or None if it isn't."""
    system = _check_supported()
    if system == "Windows":
        return _windows_status()
    if system == "Darwin":
        return _macos_status()
    return _linux_status()


def install() -> str:
    """Configure autostart. Returns what was written."""
    system = _check_supported()
    if system == "Windows":
        return _windows_install()
    if system == "Darwin":
        return _macos_install()
    return _linux_install()


def uninstall() -> bool:
    """Remove autostart. False when there was nothing to remove."""
    system = _check_supported()
    if system == "Windows":
        return _windows_uninstall()
    if system == "Darwin":
        return _macos_uninstall()
    return _linux_uninstall()


def handle(action: str) -> int:
    """Run one autostart action and print the outcome. Returns an exit code."""
    try:
        if action == "install":
            print(f"Autostart enabled: {install()}")
        elif action == "uninstall":
            if uninstall():
                print("Autostart disabled.")
            else:
                print("Autostart was not configured.")
        else:
            where = status()
            print(f"Autostart is enabled: {where}" if where else "Autostart is off.")
    except UnsupportedPlatformError as err:
        print(f"Error: {err}")
        return 1
    except OSError as err:
        print(f"Error: {err}")
        return 1
    return 0
