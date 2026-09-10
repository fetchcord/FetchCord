#!/usr/bin/env python3

# trunk-ignore(bandit/B404)
import subprocess
from importlib import resources
from pathlib import Path

# A backstop against a wedged helper taking the presence loop down with it,
# not a latency budget - so it is deliberately generous. powershell.exe cold
# start alone can take well over 15s on a slow or virtualised host (it does on
# the Windows CI runners), and WMI queries are slower still the first time.
COMMAND_TIMEOUT_SECONDS = 60


def run_command(command: list[str], shell: bool = False) -> str:
    try:
        result = subprocess.run(
            command,
            encoding="utf-8",
            errors="replace",
            stdout=subprocess.PIPE,
            # Otherwise a helper's warnings get printed over our own output.
            stderr=subprocess.DEVNULL,
            timeout=COMMAND_TIMEOUT_SECONDS,
            # trunk-ignore(bandit/B602)
            shell=shell,
        )
    except subprocess.TimeoutExpired as exc:
        raise BashError(f"Command timed out after {exc.timeout}s: {command}") from exc
    return result.stdout


def exec_bash(command: str) -> str:
    try:
        result = subprocess.run(
            command,
            encoding="utf-8",
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=COMMAND_TIMEOUT_SECONDS,
            # trunk-ignore(bandit/B602)
            shell=True,
        )
    except subprocess.TimeoutExpired as exc:
        raise BashError(f"Command timed out after {exc.timeout}s: {command}") from exc
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
    try:
        result = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-NonInteractive",
                "-Command",
                PS1_PREAMBLE + command,
            ],
            encoding="utf-8",
            # Belt and braces: a stray undecodable byte must never take down
            # the presence loop, since CommandProvider only expects BashError.
            errors="replace",
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=COMMAND_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired as exc:
        raise BashError(
            f"PowerShell command timed out after {exc.timeout}s: {command}"
        ) from exc
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
