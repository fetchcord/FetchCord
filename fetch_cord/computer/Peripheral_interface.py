#from __future__ import annotations

from abc import ABCMeta


class Peripherical_interface(metaclass=ABCMeta):
    os: str

    def __init__(self, os):
        super().__init__()
        self.os = os