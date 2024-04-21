#!/usr/bin/env python3

# trunk-ignore(bandit/B404)
import subprocess
from importlib import resources
from pathlib import Path
from typing import List


def run_command(command: List[str], shell: bool = False) -> str:
    return subprocess.run(
        command,
        encoding="utf-8",
        stdout=subprocess.PIPE,
        # trunk-ignore(bandit/B602)
        shell=shell,
    ).stdout


def exec_bash(command: str) -> str:
    return subprocess.run(
        [command],
        encoding="utf-8",
        stdout=subprocess.PIPE,
        # trunk-ignore(bandit/B602)
        shell=True,
    ).stdout.strip()


def exec_ps1(command: str) -> str:
    # trunk-ignore(bandit/B603)
    # trunk-ignore(bandit/B607)
    return subprocess.run(
        ["powershell", command], encoding="utf-8", stdout=subprocess.PIPE
    ).stdout.strip()


def get_resource_path(package, resource: str) -> Path:
    with resources.path(package, resource) as path:
        return path


class BashError(Exception):
    pass
