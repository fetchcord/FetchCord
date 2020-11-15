from __future__ import annotations
from fetch_cord.run_command import BashError, exec_bash
from typing import List
import sys

from .Gpu_interface import Gpu_interface, GpuType

GPU_VENDOR = "amd"


class Gpu_amd(Gpu_interface):
    def __init__(self, os, model):
        super().__init__(os, GPU_VENDOR, model)

    @Gpu_interface.model.setter
    def model(self, value: str):
        self._model = value

    def get_temp(self):
        if self.os == "windows":
            raise NotImplementedError(
                "Temperature report for AMD GPU's is not supported on Windows yet."
            )
        elif self.os == "macos":
            raise NotImplementedError(
                "Temperature report for AMD GPU's is not supported on MacOS yet."
            )
        elif self.os == "linux":
            raise NotImplementedError(
                "Temperature report for AMD GPU's is not supported on Linux yet."
            )
        else:
            raise NotImplementedError("Unknown OS, no GPU temperature report.")

    def get_amdgpurender(self, gpu_list: List[GpuType], laptop: bool) -> str:
        try:
            for i in range(len(gpu_list)):
                # assume DRI_PRIME=0 is the intel GPU
                if laptop and "intel" == gpu_list[i].vendor.lower():
                    i += 1
                if (
                    laptop
                    and "amd" == gpu_list[i].vendor.lower()
                    and gpu_list[i].model != self.model
                ):
                    i += 1

                env_prime = "DRI_PRIME=%s" % i
                return exec_bash(
                    "%s glxinfo | grep \"OpenGL renderer string:\" |sed 's/^.*: //;s/[(][^)]*[)]//g'"
                    % env_prime
                )
        except BashError as e:
            print("ERROR: Could not run glxinfo [%s]" % str(e))
            sys.exit(1)