from .Cpu_interface import Cpu_interface

CPU_VENDOR = 'amd'

class Cpu_amd(Cpu_interface):

    def __init__(self, os, model):
        super().__init__(os, CPU_VENDOR, model)

    @Cpu_interface.model.setter
    def model(self, value: str):
        self._model = ' '.join([value.split()[2], value.split()[3]])

    def get_temp(self):
        if self.os == 'windows':
            raise NotImplementedError("Temperature report for AMD CPU's is not supported on Windows yet.")
        elif self.os == 'macos':
            raise NotImplementedError("Temperature report for AMD CPU's is not supported on MacOS yet.")
        elif self.os == 'linux':
            raise NotImplementedError("Temperature report for AMD CPU's is not supported on Linux yet.")
        else:
            raise NotImplementedError('Unkown OS, no CPU temperature report.')
