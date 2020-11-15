import subprocess
from typing import List


def run_command(command: List[str], shell: bool = False):
    return subprocess.run(
        command, encoding="utf-8", stdout=subprocess.PIPE, shell=shell
    ).stdout
