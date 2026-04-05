#!/usr/bin/python3
import os
import re
import sys

from fetch_cord.Tools import BashError, exec_bash
from fetch_cord.args import parse_args

args = parse_args()

VALID_SYSTEMD_COMMANDS = {"start", "stop", "enable", "disable", "status"}
SERVICE_FILE_URL = (
    "https://raw.githubusercontent.com/MrPotatoBobx/FetchCord/"
    f"{'testing' if args.testing else 'master'}/systemd/fetchcord.service"
)


def validate_systemd_cmd(cmd: str) -> str:
    """Validate systemd command to prevent injection."""
    if not cmd or not isinstance(cmd, str):
        raise ValueError("Command must be a non-empty string")

    cmd = cmd.strip().lower()

    if cmd not in VALID_SYSTEMD_COMMANDS:
        raise ValueError(f"Invalid systemd command: {cmd}")

    return cmd


def get_systemd_user_dir() -> str:
    """Get the systemd user directory path."""
    home = os.path.expanduser("~")
    if not home or home == "~":
        raise ValueError("Unable to determine home directory")
    return os.path.join(home, ".local", "share", "systemd", "user")


def systemd_cmd(cmd: str):
    """Execute a systemd command with validation."""
    try:
        validated_cmd = validate_systemd_cmd(cmd)
        service_file = os.path.join(get_systemd_user_dir(), "fetchcord.service")

        exec_bash(f'systemctl --user {validated_cmd} --now "{service_file}"')
    except BashError as err:
        print(f"Error: {err}")
        sys.exit(1)
    except ValueError as err:
        print(f"Error: {err}")
        sys.exit(1)


def install():
    """Install the systemd service."""
    systemd_dir = get_systemd_user_dir()

    try:
        os.makedirs(systemd_dir, exist_ok=True)
    except OSError as err:
        print(f"Error: Cannot create directory {systemd_dir}: {err}")
        sys.exit(1)

    service_file = os.path.join(systemd_dir, "fetchcord.service")

    try:
        exec_bash(f'wget -O "{service_file}" "{SERVICE_FILE_URL}"')
    except Exception as err:
        print(f"Error: Failed to download the service file: {err}")
        sys.exit(1)

    systemd_cmd("enable")
    start()


def uninstall():
    """Uninstall the systemd service."""
    systemd_cmd("stop")
    systemd_cmd("disable")

    service_file = os.path.join(get_systemd_user_dir(), "fetchcord.service")

    try:
        if os.path.exists(service_file):
            os.remove(service_file)
    except OSError as err:
        print(f"Error: Cannot remove service file: {err}")
        sys.exit(1)

    sys.exit(0)


def enable():
    """Enable the systemd service."""
    systemd_cmd("enable")
    sys.exit(0)


def disable():
    """Disable the systemd service."""
    systemd_cmd("disable")
    sys.exit(0)


def start():
    """Start the systemd service."""
    systemd_cmd("start")
    sys.exit(0)


def stop():
    """Stop the systemd service."""
    systemd_cmd("stop")
    sys.exit(0)


def status():
    """Check the systemd service status."""
    systemd_cmd("status")
    sys.exit(0)
