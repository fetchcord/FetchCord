#!/usr/bin/python3
import os
import sys

from fetch_cord.constants import (
    DEFAULT_BRANCH,
    SERVICE_FILE_URL_TEMPLATE,
    TESTING_BRANCH,
    VALID_SYSTEMD_COMMANDS,
)
from fetch_cord.tools import BashError, exec_bash


def validate_systemd_cmd(cmd: str) -> str:
    """Validate systemd command to prevent injection."""
    if not cmd or not isinstance(cmd, str):
        raise ValueError("Command must be a non-empty string")

    cmd = cmd.strip().lower()

    if cmd not in VALID_SYSTEMD_COMMANDS:
        raise ValueError(f"Invalid systemd command: {cmd}")

    return cmd


def get_systemd_user_dir() -> str:
    home = os.path.expanduser("~")
    if not home or home == "~":
        raise ValueError("Unable to determine home directory")
    return os.path.join(home, ".local", "share", "systemd", "user")


def get_service_file_url(testing: bool = False) -> str:
    branch = TESTING_BRANCH if testing else DEFAULT_BRANCH
    return SERVICE_FILE_URL_TEMPLATE.format(branch=branch)


def systemd_cmd(cmd: str) -> None:
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


def install(testing: bool = False) -> None:
    systemd_dir = get_systemd_user_dir()

    try:
        os.makedirs(systemd_dir, exist_ok=True)
    except OSError as err:
        print(f"Error: Cannot create directory {systemd_dir}: {err}")
        sys.exit(1)

    service_file = os.path.join(systemd_dir, "fetchcord.service")
    service_url = get_service_file_url(testing)

    try:
        exec_bash(f'wget -O "{service_file}" "{service_url}"')
    except Exception as err:
        print(f"Error: Failed to download the service file: {err}")
        sys.exit(1)

    systemd_cmd("enable")
    start()


def uninstall() -> None:
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


def enable() -> None:
    systemd_cmd("enable")
    sys.exit(0)


def disable() -> None:
    systemd_cmd("disable")
    sys.exit(0)


def start() -> None:
    systemd_cmd("start")
    sys.exit(0)


def stop() -> None:
    systemd_cmd("stop")
    sys.exit(0)


def status() -> None:
    systemd_cmd("status")
    sys.exit(0)
