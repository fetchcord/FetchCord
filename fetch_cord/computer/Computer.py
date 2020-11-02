from sys import platform, exit
from typing import Dict, List
from ..run_command import run_command
from ..args import parse_args

from .cpu.get_cpu import get_cpu
from .cpu.Cpu_interface import Cpu_interface

args = parse_args()


class Computer:
    parseMap: Dict
    componentMap: Dict

    os: str
    neofetchwin: bool
    neofetch: bool
    values: str


    @property
    def memory(self) -> List[str]:
        return self.get_component("Memory:")

    @property
    def osinfo(self) -> List[str]:
        return self.get_component("OS:")

    @property
    def motherboard(self) -> List[str]:
        return self.get_component("Motherboard:")
    
    @property
    def host(self) -> List[str]:
        return self.get_component("Host:")

    @property
    def cpu(self) -> List[Cpu_interface]:
        return self.get_component("CPU:")

    @property
    def disks(self) -> List[str]:
        return self.get_component("Disk")

    @property
    def resolution(self) -> List[str]:
        return self.get_component("Resolution:")
    
    @property
    def theme(self) -> List[str]:
        return self.get_component("Theme:")

    @property
    def kernel(self) -> List[str]:
        return self.get_component("Kernel:")

    @property
    def packages(self) -> List[str]:
        return self.get_component("Packages:")
    
    @property
    def shell(self) -> List[str]:
        return self.get_component("Shell:")

    @property
    def terminal(self) -> List[str]:
        return self.get_component("Terminal:")

    @property
    def wm(self) -> List[str]:
        return self.get_component("WM:")
    
    @property
    def font(self) -> List[str]:
        return self.get_component("Font:")

    @property
    def de(self) -> List[str]:
        return self.get_component("DE:")

    def __init__(self):
        super().__init__()

        self.parseMap = {
            'CPU:': get_cpu,
            'Disk': self.get_disk,
            'Memory:': self.get_memory,
            'OS:': self.get,
            'Motherboard:': self.get,
            'Host:': self.get,
            'Resolution:': self.get,
            'Theme:': self.get,
            'Kernel:': self.get,
            'Packages:': self.get,
            'Shell:': self.get,
            'Terminal:': self.get,
            'Font:': self.get,
            'DE:': self.get,
            'WM:': self.get
        }

        self.componentMap = {}

        self.detect_os()
        self.neofetchwin, self.neofetch, self.values = self.detect_neofetch()
        self.neofetch_parser(self.values)

    def neofetch_parser(self, values: str):
        lines = values.split('\n')
        for i in range(len(lines)):
            line = lines[i]
            for key, detectedFunction in [ (key, value) for key, value in self.parseMap.items() if key in line]:
                if key not in self.componentMap:
                    self.componentMap[key] = []
                detectedFunction(self.os, self.componentMap[key], line.rstrip('\n'), key)

    def detect_os(self) -> str:
        if platform == 'linux' or platform == 'linux2':
            self.os = 'linux'
        elif platform == 'darwin':
            self.os = 'macos'
        elif platform == 'win32':
            self.os = 'windows'
        else:
            raise Exception('Not a supported OS !')

        return self.os

    def detect_neofetch(self):
        neofetchwin = False
        neofetch = False
        values = None

        if self.os == 'windows':
            try:
                values = run_command(['neofetch', '--noart'])
            except Exception:
                pass
            else:
                neofetchwin = True
        elif not neofetchwin:
            try:
                values = run_command([
                    'neofetch',
                    '--stdout',
                    '--config none' if args.noconfig else ''],
                    shell=(self.os == 'windows'))
            except Exception:
                print(
                    'ERROR: Neofetch not found, please install it or check installation and that neofetch is in PATH.')
                exit(1)
            else:
                neofetch = True
        return (
            neofetchwin, neofetch, values)

    def get_disk(self, os: str, line: List, value: str, key: str):
        """
        Append the Disk info from the given neofetch line to the Disk list

        Parameters
        ----------
        value : str
            Neofetch extracted line
        """

        line.append(value[value.find(key)+len(key)+2:])

    def get_memory(self, os: str, line: List, value: str, key: str):
        """
        Get the memory info from the given neofetch line

        Parameters
        ----------
        value : str
            Neofetch extracted line
        """

        if args.memtype == "gb":
            memgb = value.split()
            used = float(memgb[1].replace("MiB", ""))
            total = float(memgb[3].replace("MiB", ""))

            line.append(' '.join([str(round(used / 1024, 2)), "GiB /", str(round(total / 1024, 2)), "GiB"]))
        else:
            line.append(value[value.find(key)+len(key)+1:])
    
    def get(self, os: str, line: List, value: str, key: str, valueOffset: int = 1):
        """
        Get the info from the given neofetch line

        Parameters
        ----------
        os: str
            Detected OS ("windows", "linux" or "macos")
        line: List
            List who will contains the values
        value : str
            Neofetch extracted line
        key : str
            Key for the dict
        valueOffset: int
            Offset for extracting the value without the key (default : 1)
        """

        line.append(value[value.find(key)+len(key)+valueOffset:])

    def get_component(self, key: str):
        try:
            return self.componentMap[key]
        except KeyError as err:
            print("[KeyError]: ", end="")
            print(err)

            return []