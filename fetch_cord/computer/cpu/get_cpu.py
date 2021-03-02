#from __future__ import annotations

from typing import List

from .Cpu_amd import Cpu_amd
from .Cpu_intel import Cpu_intel


def get_cpu(os: str, line: List, value: str, key: str):
    """
    Append the CPU info from the given neofetch line to the CPU list

    Parameters
    ----------
    os :
        OS type
    line : List
        Component line
    value : str
        Neofetch extracted line
    key : str
        Component key
    """

    vendor = value.replace(key, "").lstrip("").replace("Intel(R)", "Intel")

    if vendor.find("Intel") != -1 or vendor.find("Pentium") != -1:
        line.append(Cpu_intel(os, value))
    elif vendor.find("AMD") != -1:
        line.append(Cpu_amd(os, value))