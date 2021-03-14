#!/usr/bin/python3

from os import system
from ..run_command import BashError, exec_bash
from ..args import parse_args
import sys

args = parse_args()


def systemd_cmd(cmd: str):
    try:
        print(exec_bash(f"systemctl --user {cmd} --now fetchcord"))
    except BashError as err:
        print(err)
        sys.exit(1)


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

    systemd_cmd("enable")

    start()


def uninstall():
    systemd_cmd("stop")

    systemd_cmd("disable")

    try:
        exec_bash("rm -f ~/.local/share/systemd/user/fetchcord.service")
    except:
        print("Error : Cannot remove service file...")
        sys.exit(1)

    sys.exit(0)


def enable():
    systemd_cmd("enable")
    sys.exit(0)


def disable():
    systemd_cmd("disable")
    sys.exit(0)


def start():
    systemd_cmd("start")
    sys.exit(0)


def stop():
    systemd_cmd("stop")
    sys.exit(0)


def status():
    systemd_cmd("status")
    sys.exit(0)