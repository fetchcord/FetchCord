#!/usr/bin/env python3

from pathlib import Path
import subprocess
from typing import List

from importlib import resources


def run_command(command: List[str], shell: bool = False) -> str:
    return subprocess.run(
        command, encoding="utf-8", stdout=subprocess.PIPE, shell=shell
    ).stdout


def exec_bash(command: str) -> str:
    return subprocess.run(
        [command], encoding="utf-8", stdout=subprocess.PIPE, shell=True
    ).stdout.strip()


def exec_ps1(command: str) -> str:
    return subprocess.run(
        ["powershell", command], encoding="utf-8", stdout=subprocess.PIPE, shell=True
    ).stdout.strip()


def get_resource_path(package, resource: str) -> Path:
    with resources.path(package, resource) as path:
        return path
