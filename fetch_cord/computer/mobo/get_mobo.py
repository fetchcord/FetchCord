from fetch_cord.run_command import exec_bash
from typing import List


def get_mobo(os: str, line: List, value: str, key: str):
    if os == "linux":
        line.append(exec_bash("cat /sys/devices/virtual/dmi/id/board_vendor"))
    else:
        line.append(value[value.find(key) + len(key) + 1 :])