# from __future__ import annotations

import os
from pathlib import Path

from fetch_cord.Tools import BashError, exec_bash


def get_home_dir() -> Path:
    """Get and validate the home directory."""
    home = os.getenv("HOME")
    if not home:
        raise ValueError("HOME environment variable is not set")
    home_path = Path(home)
    if not home_path.is_absolute():
        raise ValueError("HOME environment variable must be an absolute path")
    if not home_path.exists():
        raise ValueError(f"Home directory does not exist: {home}")
    return home_path


def enableFlatpak():
    try:
        home = get_home_dir()
    except ValueError as e:
        print(f"Error: {e}")
        return

    flatpak_discord_path = home / ".var" / "app" / "com.discordapp.Discord"
    package_path = Path("/usr/bin/discord")
    manual_install_path = Path("/opt/Discord")

    if (
        flatpak_discord_path.is_dir()
        and not package_path.exists()
        and not manual_install_path.exists()
    ):
        XDG_Symlink(home)


def XDG_Symlink(home: Path):
    try:
        print("Symlinking XDG_RUNTIME_DIR path for Flatpak Discord.")
        var_dir = home / ".var"
        if not var_dir.exists():
            print(f"Error: {var_dir} does not exist")
            return
        exec_bash(
            f'cd "{var_dir}" && ln -sf "{{app/com.discordapp.Discord,$XDG_RUNTIME_DIR}}/discord-ipc-0"'
        )
    except BashError as e:
        print(f"Could not symlink XDG_RUNTIME_DIR Error: {e}")
