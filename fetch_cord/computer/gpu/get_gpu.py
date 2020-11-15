from typing import List

from .Gpu_amd import Gpu_amd
from .Gpu_nvidia import Gpu_nvidia
from .Gpu_intel import Gpu_intel


def get_gpu(os: str, line: List, value: str, key: str):
    """
    Append the GPU info from the given neofetch line to the GPU list

    Parameters
    ----------
    value : str
        Neofetch extracted line
    """

    value = value.replace(key, "").lstrip("")
    splitValue = value.split()

    if any(x.upper() in splitValue for x in ["AMD", "RADEON"]):
        line.append(Gpu_amd(os, value))
    elif any(x.upper() in splitValue for x in ["NVIDIA", "GEFORCE"]):
        line.append(Gpu_nvidia(os, value))
    elif any(x.upper() in splitValue for x in ["INTEL"]):
        line.append(Gpu_intel(os, value))