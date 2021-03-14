# from __future__ import annotations

import logging
from sys import platform, exit
import sys
from typing import Callable, Dict, List, Tuple
import psutil, os

from ..run_command import exec_bash, run_command
from ..args import parse_args
from ..Logger import Logger
from .flatpak import enableFlatpak
from .resources import get_infos, get_default_config
from .cpu.get_cpu import get_cpu
from .cpu.Cpu_interface import Cpu_interface
from .gpu.get_gpu import get_gpu
from .gpu.Gpu_interface import GpuType, get_gpuid

args = parse_args()

logger = Logger(
    "fetchcord_computer.log",
    "fetchcord_computer",
    logging.DEBUG if args.debug else logging.INFO,
)


class Computer:
    parseMap: Dict[str, Callable]
    componentMap: Dict[str, List] = {}
    idsMap: Dict[str, Dict]

    os: str
    neofetchwin: bool = False
    neofetch: bool = False
    values: str
    laptop: bool = False
    uptime: float

    @property
    def memory(self) -> str:
        return self.get_component_line("Memory:")

    @property
    def osinfo(self) -> str:
        return self.get_component_line("OS:")

    @property
    def osinfoid(self) -> str:
        component = self.get_component_line("OS:")
        component = (component.split()[0] + component.split()[1]).lower()
        component_list = self.idsMap[self.idsMap["map"]["OS:"]]

        for comp, id in component_list.items():
            if component.lower().find(comp.lower()) >= 0:
                return id

        print(
            "Unknown {}, contact us on github to resolve this.".format(
                self.idsMap["map"]["OS:"]
            )
        )

        return component_list["unknown"]

    @property
    def motherboard(self) -> str:
        return self.get_component_line("Motherboard:")

    @property
    def motherboardid(self) -> str:
        return self.get_component_idkey("Motherboard:")

    @property
    def host(self) -> str:
        return self.get_component_line("Host:")

    @property
    def hostid(self) -> str:
        hostsplit = self.host.split()
        host_list: Dict[str, str] = self.idsMap[self.idsMap["map"]["Host:"]]

        for line in hostsplit:
            if line in host_list:
                return line

        # try to get MacBook hostid
        hostid = []
        hostjoin = " ".join(self.host)
        for numsplit in range(len(hostjoin)):
            if not hostjoin[numsplit].isdigit():
                hostid.append(hostjoin[numsplit])
        hostid = "".join(hostid)
        hostid = hostid.split()[1]

        if hostid in host_list:
            return host_list[hostid]
        else:
            return host_list["unknown"]

    @property
    def hostappid(self) -> str:
        return self.get_component_id("Host:")

    @property
    def cpu(self) -> str:
        key = "CPU:"
        cpus: List[Cpu_interface] = self.get_component(key)
        temp = []
        for cpu in cpus:
            temp.append(cpu.info)

        return "\n".join(temp) if len(cpus) > 0 else "{} N/A".format(key)

    @property
    def cpuid(self) -> str:
        temp: List[Cpu_interface] = self.get_component("CPU:")

        if len(temp) == 0:
            return self.idsMap[self.idsMap["map"]["CPU:"]]["unknown"]
        else:
            return temp[0].get_id(self.idsMap[self.idsMap["map"]["CPU:"]])

    @property
    def gpu(self) -> str:
        key = "GPU:"
        gpus: List[GpuType] = self.get_component(key)
        temp = []
        for gpu in gpus:
            if gpu.vendor == "amd" and self.os == "linux":
                temp.append(gpu.get_amdgpurender(gpus, self.laptop).rstrip().lstrip())
            else:
                temp.append(gpu.model.lstrip().rstrip())

        return "\n".join(temp) if len(gpus) > 0 else "{} N/A".format(key)

    @property
    def gpuid(self) -> str:
        return get_gpuid(
            self.idsMap[self.idsMap["map"]["GPU:"]], self.get_component("GPU:")
        )

    @property
    def disks(self) -> str:
        return self.get_component_line("Disk")

    @property
    def resolution(self) -> str:
        return self.get_component_line("Resolution:")

    @property
    def theme(self) -> str:
        return self.get_component_line("Theme:")

    @property
    def kernel(self) -> str:
        return self.get_component_line("Kernel:")

    @property
    def packages(self) -> str:
        return self.get_component_line("Packages:")

    @property
    def shell(self) -> str:
        return self.get_component_line("Shell:")

    @property
    def shellid(self) -> str:
        return self.get_component_id("Shell:")

    @property
    def terminal(self) -> str:
        return self.get_component_line("Terminal:")

    @property
    def terminalid(self) -> str:
        return self.get_component_id("Terminal:")

    @property
    def wm(self) -> str:
        return self.get_component_line("WM:")

    @property
    def wmid(self) -> str:
        return self.get_component_line("WM:").split()[0]

    @property
    def font(self) -> str:
        return self.get_component_line("Font:")

    @property
    def de(self) -> str:
        return self.get_component_line("DE:")

    @property
    def deid(self) -> str:
        value = self.get_component_line("DE:").split()[0]

        return "n/a" if value == "DE:" else value

    @property
    def dewmid(self) -> str:
        de = self.get_component_line("DE:")

        return "\n".join(
            ["" if de == "{} N/A".format("DE:") else de, self.get_component_line("WM:")]
        )

    @property
    def desktopid(self) -> str:
        deid = self.deid.lower()
        wmid = self.wmid.lower()

        if deid == "unity":
            if wmid == "compiz":
                return "unity"
            else:
                return wmid

        if deid != "n/a" and deid in self.idsMap[self.idsMap["map"]["DE:"]]:
            return deid
        elif deid == "n/a" and wmid in self.idsMap[self.idsMap["map"]["WM:"]]:
            return wmid
        else:
            print("Unknown DE/WM, contact us on github to resolve this.")
            return "unknown"

    @property
    def battery(self) -> str:
        if self.laptop:
            return self.get_component_line("Battery")
        else:
            return "{} N/A".format("Battery")

    @property
    def lapordesk(self) -> str:
        if self.laptop and self.os != "macos":
            return "laptop"
        else:
            return "desktop"

    @property
    def version(self) -> str:
        return os.popen("sw_vers -productVersion").read()

    @property
    def product(self) -> str:
        return os.popen("sysctl -n hw.model").read()

    @property
    def devicetype(self) -> str:
        if self.product[0:7] == "MacBook":
            return "laptop"
        else:
            return "desktop"

    @property
    def bigicon(self) -> str:
        try:
            return self.idsMap[self.idsMap["map"]["Version:"]][self.version[0:5]]
        except KeyError:
            print("Unsupported MacOS version")
            return "bigslurp"

    def __init__(self):
        super().__init__()

        self.parseMap = {
            "CPU:": get_cpu,
            "GPU:": get_gpu,
            "Disk": self.get_disk,
            "Memory:": self.get_memory,
            "OS:": self.get,
            "Motherboard:": self.get,
            "Host:": self.get,
            "Resolution:": self.get,
            "Theme:": self.get,
            "Kernel:": self.get,
            "Packages:": self.get,
            "Shell:": self.get,
            "Terminal:": self.get,
            "Font:": self.get,
            "DE:": self.get,
            "WM:": self.get,
            "Battery": self.get_battery,
        }

        self.idsMap = get_infos()
        self.uptime = psutil.boot_time()

        self.detect_os()
        self.detect_laptop()

        self.fetch_values()

    def fetch_values(self):
        self.neofetchwin, self.neofetch, self.values = self.detect_neofetch()

        self.neofetch_parser(self.values)

        if not bool(self.componentMap):
            args.config_path = ""
            args.noconfig = False

            self.neofetchwin, self.neofetch, self.values = self.detect_neofetch()
            self.neofetch_parser(self.values)

        terminallist = self.idsMap[self.idsMap["map"]["Terminal:"]]
        if args.terminal and args.terminal.lower() in terminallist:
            self.componentMap["Terminal:"] = [args.terminal.lower()]
        elif args.terminal and args.terminal.lower() not in terminallist:
            print(
                "\nInvalid terminal, only %s are supported.\n"
                "Please make a github issue if you would like to have your terminal added.\n"
                "https://github.com/MrPotatoBobx/FetchCord" % terminallist
            )
            sys.exit(1)

        if self.get_component("Font:", True) and args.termfont:
            print(
                "Custom terminal font not set because a terminal font already exists, %s"
                % self.font
            )
        elif not self.get_component("Font:", True) and args.termfont:
            self.componentMap["Font:"] = [args.termfont]

    def updateMap(self):
        """
        Clear the components values and fetch new ones
        """
        self.clearMap()
        self.neofetchwin, self.neofetch, self.values = self.detect_neofetch()
        self.neofetch_parser(self.values)

    def clearMap(self):
        """
        Clear the components values
        """
        for key in self.componentMap.keys():
            del self.componentMap[key][:]

    def neofetch_parser(self, values: str):
        if args.debug:
            print(values)
        lines = values.split("\n")
        for i in range(len(lines)):
            line = lines[i]
            for key, detectedFunction in [
                (key, value) for key, value in self.parseMap.items() if key in line
            ]:
                if key not in self.componentMap:
                    self.componentMap[key] = []
                detectedFunction(
                    self.os, self.componentMap[key], line.rstrip("\n"), key
                )

    def detect_os(self) -> str:
        if platform == "linux" or platform == "linux2":
            self.os = "linux"
        elif platform == "darwin":
            self.os = "macos"
        elif platform == "win32":
            self.os = "windows"
        else:
            raise Exception("Not a supported OS !")

        return self.os

    def detect_laptop(self) -> bool:
        if self.os != "linux":
            self.laptop = False
        else:
            for i in os.listdir("/sys/class/power_supply"):
                if i.startswith("BAT"):
                    self.laptop = True
                    break

        return self.laptop

    def detect_neofetch(self):
        neofetchwin = False
        neofetch = False
        values = None

        if self.os == "windows":
            try:
                values = run_command(["neofetch", "--noart"])
            except Exception:
                pass
            else:
                neofetchwin = True
        elif not neofetchwin:
            if self.os == "linux":
                enableFlatpak()

            default_config = get_default_config()

            try:
                if self.os == "windows":
                    values = run_command(
                        [
                            "neofetch",
                            "--config {}".format(
                                "none"
                                if args.noconfig
                                else (
                                    args.config_path
                                    if args.config_path
                                    else (default_config)
                                )
                            ),
                            "--stdout",
                        ],
                        shell=(self.os == "windows"),
                    )
                else:
                    values = exec_bash(
                        "neofetch --config {} --stdout".format(
                            "none"
                            if args.noconfig
                            else (
                                args.config_path
                                if args.config_path
                                else (default_config)
                            )
                        )
                    )
                if args.nfco:
                    with open(args.nfco) as f:
                        values = "\n".join(f.readlines())
                
            except Exception:
                print(
                    "ERROR: Neofetch not found, please install it or check installation and that neofetch is in PATH."
                )
                exit(1)
            else:
                neofetch = True

        return (neofetchwin, neofetch, values)

    def get_battery(self, os: str, line: List, value: str, key: str):
        """
        Append the Battery info from given neofetch line

        Parameters
        ----------
        value : str
            Neofetch extracted line
        """

        line.append(value[value.find(key) + len(key) + 2 :])

    def get_disk(self, os: str, line: List, value: str, key: str):
        """
        Append the Disk info from the given neofetch line to the Disk list

        Parameters
        ----------
        value : str
            Neofetch extracted line
        """

        line.append(value[value.find(key) + len(key) + 2 :])

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

            line.append(
                " ".join(
                    [
                        str(round(used / 1024, 2)),
                        "GiB /",
                        str(round(total / 1024, 2)),
                        "GiB",
                    ]
                )
            )
        else:
            line.append(value[value.find(key) + len(key) + 1 :])

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

        line.append(value[value.find(key) + len(key) + valueOffset :])

    def get_component(self, key: str, quiet: bool = False):
        """
        Get component info from map

        Args:
            key (str): component key in map
        """
        try:
            return self.componentMap[key]
        except KeyError as err:
            if quiet:
                print("[KeyError]: {}".format(err), end="")

            return []

    def get_component_line(self, key: str) -> str:
        try:
            values = self.componentMap[key]
            return "\n".join(values) if len(values) > 0 else "{} N/A".format(key)
        except KeyError as err:
            print("[KeyError]: ", end="")
            print(err)

            return "{} N/A".format(key)

    def get_component_id(self, key: str) -> str:
        component = self.get_component_line(key).lower()
        component_list = self.idsMap[self.idsMap["map"][key]]

        for comp, id in component_list.items():
            if component.find(comp.lower()) >= 0:
                return id

        print(
            "Unknown {}, contact us on github to resolve this.".format(
                self.idsMap["map"][key]
            )
        )

        return component_list["unknown"]

    def get_component_idkey(self, key: str) -> str:
        component = self.get_component_line(key).lower()
        component_list = self.idsMap[self.idsMap["map"][key]]

        for comp, _ in component_list.items():
            if component.find(comp.lower()) >= 0:
                return comp

        print(
            "Unknown {}, contact us on github to resolve this.".format(
                self.idsMap["map"][key]
            )
        )

        return component_list["unknown"]
