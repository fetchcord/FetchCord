from __future__ import annotations
from abc import ABCMeta, abstractmethod
from typing import List, TypeVar, Dict

from ..Peripheral_interface import Peripherical_interface


class Gpu_interface(Peripherical_interface, metaclass=ABCMeta):
    vendor: str
    _model: str

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


GpuType = TypeVar("GpuType", bound="Gpu_interface")


def get_gpuid(gpu_ids: Dict[str, str], gpus: List[GpuType]):
    vendors = []
    for i in range(len(gpus)):
        if gpus[i].model.split()[0] not in vendors:
            vendors.append(gpus[i].model.split()[0])

    gpuvendor = "".join(vendors).lower()

    if gpuvendor in gpu_ids:
        return gpu_ids[gpuvendor]
    else:
        print("Unknown GPU, contact us on github to resolve this.")
        return "unknown"
