from __future__ import annotations
from fetch_cord.run_command import BashError, exec_bash
from .Gpu_interface import Gpu_interface

GPU_VENDOR = "nvidia"


class Gpu_nvidia(Gpu_interface):
    primeoffload: bool

    def __init__(self, os, model):
        super().__init__(os, GPU_VENDOR, model)

    @Gpu_interface.model.setter
    def model(self, value: str):
        self._model = value

    def get_temp(self):
        if self.os == "windows":
            raise NotImplementedError(
                "Temperature report for Nvidia GPU's is not supported on Windows yet."
            )
        elif self.os == "macos":
            raise NotImplementedError(
                "Temperature report for Nvidia GPU's is not supported on MacOS yet."
            )
        elif self.os == "linux":
            try:
                return exec_bash(
                    "nvidia-smi -q | awk '/GPU Current Temp/{print $5}' | sed 's/^/[/;s/$/°C]/'"
                )
            except BashError:
                pass
        else:
            raise NotImplementedError("Unknown OS, no GPU temperature report.")

    def check_primeoffload(self):
        # only show the GPU in use with optimus, show both if prime render offload
        self.primeoffload = False
        try:
            self.primeoffload = exec_bash('xrandr --listproviders | grep -o "NVIDIA-0"')
            return True
        except BashError:
            return False