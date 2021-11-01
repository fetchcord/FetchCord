#from __future__ import annotations

from fetch_cord.run_command import BashError, exec_bash
import os


def enableFlatpak():
    home = os.getenv("HOME")
    flatpak_discord_path = os.path.isdir("%s/.var/app/com.discordapp.Discord" % home)
    package_path = os.path.isfile("/usr/bin/discord")
    manual_install_path = os.path.isdir("/opt/Discord")
    if flatpak_discord_path and not package_path and not manual_install_path:
        XDG_Symlink(home)


def XDG_Symlink(home):
    try:
        print("Symlinking XDG_RUNTIME_DIR path for Flatpak Discord.")
        exec_bash(
            "cd %s/.var && ln -sf {app/com.discordapp.Discord,$XDG_RUNTIME_DIR}/discord-ipc-0 "
            % home
        )
    except BashError as e:
        print("Could not symlink XDG_RUNTIME_DIR Error: %s" % str(e))
        return
