#!/usr/bin/env python3

# trunk-ignore(bandit/B404)
import subprocess
from importlib import resources
from pathlib import Path


def run_command(command: list[str], shell: bool = False) -> str:
    return subprocess.run(
        command,
        encoding="utf-8",
        stdout=subprocess.PIPE,
        # trunk-ignore(bandit/B602)
        shell=shell,
    ).stdout


def exec_bash(command: str) -> str:
    result = subprocess.run(
        command,
        encoding="utf-8",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        # trunk-ignore(bandit/B602)
        shell=True,
    )
    if result.returncode != 0:
        raise BashError(f"Command failed (exit {result.returncode}): {command}")
    return result.stdout.strip()


def exec_ps1(command: str) -> str:
    # trunk-ignore(bandit/B603)
    # trunk-ignore(bandit/B607)
    result = subprocess.run(
        ["powershell", command],
        encoding="utf-8",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if result.returncode != 0:
        raise BashError(
            f"PowerShell command failed (exit {result.returncode}): {command}"
        )
    return result.stdout.strip()


def get_resource_path(package: str, resource: str) -> Path:
    with resources.path(package, resource) as path:
        return path


class BashError(Exception):
    pass
