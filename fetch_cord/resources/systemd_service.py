#!/usr/bin/python3

from ..run_command import BashError, exec_bash
from ..args import parse_args
import sys

args = parse_args()


def install():
    try:
        exec_bash("mkdir -p ~/.local/share/systemd/user")
    except:
        print("Error : Cannot create directory...")
        sys.exit(1)

    try:
        exec_bash(
            f"wget -O ~/.local/share/systemd/user/fetchcord.service https://raw.githubusercontent.com/MrPotatoBobx/FetchCord/{'testing' if args.testing else 'master'}/systemd/fetchcord.service",
        )
    except:
        print("Error: Failed to download the service file.")
        sys.exit(1)

    try:
        exec_bash("systemctl --user enable --now fetchcord")
    except:
        print("Error: failed to enable systemd service.")
        sys.exit(1)

    try:
        exec_bash("systemctl --user start --now fetchcord")
    except:
        print("Error: failed to start systemd service.")
        sys.exit(1)

    sys.exit(0)


def uninstall():
    try:
        exec_bash("systemctl --user stop --now fetchcord")
    except:
        print("Error: failed to stop systemd service.")
        sys.exit(1)

    try:
        exec_bash("systemctl --user disable --now fetchcord")
    except:
        print("Error: failed to disable systemd service.")
        sys.exit(1)

    try:
        exec_bash("rm -f ~/.local/share/systemd/user/fetchcord.service")
    except:
        print("Error : Cannot remove service file...")
        sys.exit(1)

    sys.exit(0)


def start():
    try:
        print(exec_bash("systemctl --user start --now fetchcord"))
    except BashError as err:
        print(err)
        sys.exit(1)
    sys.exit(0)


def stop():
    try:
        print(exec_bash("systemctl --user stop --now fetchcord"))
    except BashError as err:
        print(err)
        sys.exit(1)
    sys.exit(0)


def status():
    try:
        print(exec_bash("systemctl --user status --now fetchcord"))
    except BashError as err:
        print(err)
        sys.exit(1)
    sys.exit(0)