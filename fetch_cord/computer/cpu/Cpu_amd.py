#from __future__ import annotations

import os
from sys import platform

if os.name != "nt" and platform != "darwin":
    from psutil import sensors_temperatures
from .Cpu_interface import Cpu_interface

CPU_VENDOR = "amd"


class Cpu_amd(Cpu_interface):
    def __init__(self, os, model):
        super().__init__(os, CPU_VENDOR, model)

    @Cpu_interface.model.setter
    def model(self, value: str):
        self.info = " ".join(value.split()[1:])
        self._model = " ".join([value.split()[2], value.split()[3]])

        if self._model.find("APU") != -1:
            self._model = f"{self._model.split('-')[0]} APU"


    def get_temp(self) -> float:
        if self.os == "windows":
            raise NotImplementedError(
                "Temperature report for AMD CPU's is not supported on Windows yet."
            )
        elif self.os == "macos":
            raise NotImplementedError(
                "Temperature report for AMD CPU's is not supported on MacOS yet."
            )
        elif (
            self.os == "linux" # and os.name != "nt" linux only
        ):  # os.name comparaison not needed, its just for the linter
            sensors = sensors_temperatures()
            if "k10temp" in sensors:
                temps = sensors["k10temp"]
                if len(temps) == 1:
                    return temps.current
                else:
                    for temp in temps:
                        if temp.label == "Tdie":
                            return temp.current

                raise Exception("No valid temperature value found.")

            raise Exception("No valid sensor found.")
        else:
            raise NotImplementedError("Unknown OS, no CPU temperature report.")
