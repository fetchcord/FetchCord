#from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import Dict

from ..Peripheral_interface import Peripherical_interface


class Cpu_interface(Peripherical_interface, metaclass=ABCMeta):
    vendor: str
    _model: str
    info: str

    @property
    def model(self) -> str:
        return self._model

    @model.setter
    @abstractmethod
    def model(self, value: str):
        raise NotImplementedError

    @property
    def temp(self) -> float:
        try:
            self._temp = self.get_temp()
        except NotImplementedError as e:
            try:
                raise e
            finally:
                e = None
                del e

        else:
            return self._temp

    @temp.setter
    def temp(self, value: float):
        self._temp = value

    def __init__(self, os, vendor, model):
        super().__init__(os)
        self.vendor = vendor
        self.model = model

    @abstractmethod
    def get_temp(self) -> float:
        raise NotImplementedError

    def get_id(self, cpu_list: Dict[str, str]) -> str:
        if self.model.lower() in cpu_list[self.vendor]:
            return cpu_list[self.vendor][self.model.lower()]
        else:
            return cpu_list["unknown"]
