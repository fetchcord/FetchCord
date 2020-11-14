from .Gpu_interface import Gpu_interface
import re

GPU_VENDOR = 'nvidia'

class Gpu_nvidia(Gpu_interface):

    def __init__(self, os, model):
        super().__init__(os, GPU_VENDOR, model)

    @Gpu_interface.model.setter
    def model(self, value: str):
        pass

    def get_temp(self):
        if self.os == 'windows':
            raise NotImplementedError("Temperature report for Nvidia GPU's is not supported on Windows yet.")
        elif self.os == 'macos':
            raise NotImplementedError("Temperature report for Nvidia GPU's is not supported on MacOS yet.")
        elif self.os == 'linux':
            raise NotImplementedError("Temperature report for Nvidia GPU's is not supported on Linux yet.")
        else:
            raise NotImplementedError('Unknown OS, no GPU temperature report.')
