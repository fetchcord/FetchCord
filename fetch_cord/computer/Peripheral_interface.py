import subprocess
from abc import ABCMeta, abstractmethod

class Peripherical_interface(metaclass=ABCMeta):
    os: str

    def __init__(self, os):
        super().__init__()
        self.os = os