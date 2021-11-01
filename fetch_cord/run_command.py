#from __future__ import annotations

from typing import List
import subprocess


def run_command(command: List[str], shell: bool = False):
    return subprocess.run(
        command, encoding="utf-8", stdout=subprocess.PIPE, shell=shell
    ).stdout


class BashError(Exception):
    pass


def exec_bash(command: str):
    try:
        out = (
            subprocess.check_output(["bash", "-c", command], stderr=subprocess.STDOUT)
            .decode("utf8")
            .strip()
        )

    except subprocess.CalledProcessError as e:
        out = e.stdout.decode("utf8")
        raise BashError("Failed to execute '%s' :\n%s" % (command, out))
    except FileNotFoundError as e:
        raise BashError("BASH not installed on your computer...")

    return out
