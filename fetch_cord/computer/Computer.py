from sys import platform, exit
from typing import Dict, List
from ..run_command import run_command
from ..args import parse_args
from .cpu import Cpu_intel
from .cpu import Cpu_amd

args = parse_args()


class Computer:
    parseMap: Dict

    neofetchwin: bool
    neofetch: bool
    values: str

    componentMap: Dict
    os: str
    osinfo: str
    cpulist: List
    disklist: List[str]
    memory: str
    motherboard: str

    def __init__(self):
        super().__init__()

        self.parseMap = {
            'CPU:': self.get_cpu,
            'Disk': self.get_disk,
            'Memory:': self.get_memory,
            'OS:': self.get_os,
            'Motherboard:': self.get_mobo
        }
        self.cpulist = []
        self.disklist = []
        self.memory = ""
        self.osinfo = ""
        self.motherboard = ""

        self.detect_os()
        self.neofetchwin, self.neofetch, self.values = self.detect_neofetch()
        self.neofetch_parser(self.values)

    def neofetch_parser(self, values: str):
        lines = values.split('\n')
        for i in range(len(lines)):
            line = lines[i]
            for key, detectedFunction in [ (key, value) for key, value in self.parseMap.items() if key in line]:
                detectedFunction(line.rstrip('\n'), key)

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

    def get_cpu(self, value: str, key: str):
        """
        Append the CPU info from the given neofetch line to the CPU list

        Parameters
        ----------
        value : str
            Neofetch extracted line
        """

        vendor = value.split()[1].replace('Intel(R)', 'Intel')

        if vendor == 'Intel' or vendor == 'Pentium':
            self.cpulist.append(Cpu_intel.Cpu_intel(self.os, value))
        else:
            if vendor.find('AMD') != -1:
                self.cpulist.append(Cpu_amd.Cpu_amd(self.os, value))

    def get_disk(self, value: str, key: str):
        """
        Append the Disk info from the given neofetch line to the Disk list

        Parameters
        ----------
        value : str
            Neofetch extracted line
        """
        self.disklist.append(value[value.find(key)+len(key)+2:])

    def get_memory(self, value: str, key: str):
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

            self.memory = ' '.join([str(round(used / 1024, 2)), "GiB /", str(round(total / 1024, 2)), "GiB"])
        else:
            self.memory = value[value.find(key)+len(key)+1:]

    def get_os(self, value: str, key: str):
        """
        Get the os info from the given neofetch line

        Parameters
        ----------
        value : str
            Neofetch extracted line
        """

        self.osinfo = value[value.find(key)+len(key)+1:]

    def get_mobo(self, value: str, key: str):
        """
        Get the mobo info from the given neofetch line

        Parameters
        ----------
        value : str
            Neofetch extracted line
        """

        self.motherboard = value[value.find(key)+len(key)+1:]