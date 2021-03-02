from __future__ import annotations
from typing import List

from .Gpu_amd import Gpu_amd
from .Gpu_nvidia import Gpu_nvidia
from .Gpu_intel import Gpu_intel


def get_gpu(os: str, line: List, value: str, key: str):
    """
    Append the GPU info from the given neofetch line to the GPU list

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

    value = value.replace(key, "").lstrip("")
    splitValue = value.split()

    for v in splitValue:
        if v.upper() in ["AMD", "RADEON"]:
            line.append(Gpu_amd(os, value))
            return
        elif v.upper() in ["NVIDIA", "GEFORCE"]:
            line.append(Gpu_nvidia(os, value))
            return
        elif v.upper() in ["INTEL"]:
            line.append(Gpu_intel(os, value))
            return