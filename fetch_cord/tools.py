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


# Windows PowerShell 5.1 writes its output in the console's OEM code page
# (cp437/cp850/cp1252 depending on locale), not UTF-8. Pinning the output
# encoding from inside the session makes the bytes we get back match the
# encoding we decode them with, on any locale.
PS1_PREAMBLE = "[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; "


def exec_ps1(command: str) -> str:
    # trunk-ignore(bandit/B603)
    # trunk-ignore(bandit/B607)
    result = subprocess.run(
        [
            "powershell",
            "-NoProfile",
            "-NonInteractive",
            "-Command",
            PS1_PREAMBLE + command,
        ],
        encoding="utf-8",
        # Belt and braces: a stray undecodable byte must never take down the
        # presence loop, since CommandProvider only expects BashError.
        errors="replace",
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
