#from __future__ import annotations

from .Cpu_interface import Cpu_interface
import re

CPU_VENDOR = "intel"


class Cpu_intel(Cpu_interface):
    def __init__(self, os, model):
        super().__init__(os, CPU_VENDOR, model)

    @Cpu_interface.model.setter
    def model(self, value: str):
        self.info = " ".join(value.split()[1:])
        if value.split()[1].replace("Intel(R)", "Intel") == "Pentium":
            self._model = value.split()[1]
        else:
            # Remove "CPU: ", "(R)" and "(TM)"
            self._model = " ".join(
                re.sub(r"\((.+)\)", "", value.replace("-", " ")).split()[1:]
            )

            # Core 2 Duo, Core 2 Quad
            if self._model.find("Intel Core") != -1:
                self._model = " ".join(self._model.split()[:4])
            else:
                self._model = " ".join(self._model.split()[:2])

            if self._model == "Intel Core":
                self._model = value.split()[1:5]
                self._model = " ".join(self._model)

    def get_temp(self):
        if self.os == "windows":
            raise NotImplementedError(
                "Temperature report for Intel CPU's is not supported on Windows yet."
            )
        elif self.os == "macos":
            raise NotImplementedError(
                "Temperature report for Intel CPU's is not supported on MacOS yet."
            )
        elif self.os == "linux":
            raise NotImplementedError(
                "Temperature report for Intel CPU's is not supported on Linux yet."
            )
        else:
            raise NotImplementedError("Unkown OS, no CPU temperature report.")
