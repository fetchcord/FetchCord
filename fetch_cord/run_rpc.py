# Import cool new rpc module that gives us more control and gets rid of headaches :)
from typing import Callable, Dict
from pypresence import Presence, exceptions
import time
import sys
import os
import psutil
# import info about system
from .args import parse_args
from .config import ConfigError, load_config
from .debugger import run_rpc_debug
from .computer.Computer import Computer

args = parse_args()

uptime = psutil.boot_time()
# discord uses unix time to interpret time for rich presence, this is uptime in unix time
start_time = float(uptime)


class Run_rpc:
    rpcs: Dict
    config: Dict

    loops: Dict
    loops_indexes: Dict
    poll_rate: int
    update: Callable

    def __init__(self):
        self.rpcs = {}

        try:
            self.config = load_config()
        except ConfigError as e:
            print("Error loading config file, using default values." % str(e))

        # self.try_connect()

    def set_loop(self, loops: Dict, loops_indexes: Dict, update: Callable, poll_rate: int = 3):
        self.loops = loops
        self.loops_indexes = loops_indexes

        self.poll_rate = poll_rate
        self.update = update

    def run_loop(self, computer: Computer):
        try:
            loop = 0
            while True:
                for i in range(len(self.loops_indexes)):
                    if loop == self.poll_rate:
                        self.update(self, computer)
                        loop = 0
                    try:
                        client_id, func = self.loops[self.loops_indexes[i]]

                        if self.loops_indexes[i] not in self.rpcs:
                            self.rpcs[self.loops_indexes[i]
                                      ] = Presence(client_id)
                            self.try_connect(self.loops_indexes[i])

                        func(self, self.loops_indexes[i], computer)
                    except ConnectionResetError:
                        self.try_connect(self.loops_indexes[i])
        except KeyboardInterrupt:
            print("Closing connection.")
            sys.exit(0)

    def try_connect(self, key: str):
        while True:
            try:
                self.rpcs[key].connect()
                break
            except ConnectionRefusedError:
                print(
                    "RPC connection refused (is Discord open?); trying again in 30 seconds")
                time.sleep(30)

    def try_clear(self, key: str):
        try:
            self.rpcs[key].clear(pid=os.getpid())
        except exceptions.InvalidID:
            pass

    def try_update(self, key: str, state, details, large_image, large_text, small_image, small_text, start):
        try:
            self.rpcs[key].update(state=state, details=details, large_image=large_image,
                                  large_text=large_text, small_image=small_image, small_text=small_text,
                                  start=start)
        # ConnectionResetError is here to avoid crashing if Discord is still just starting
        except (ConnectionResetError, exceptions.InvalidID):
            pass


def main():
    computer: Computer = Computer()

    if not computer.neofetchwin and computer.host == "Host: N/A" and args.nodistro and args.noshell and args.nohardware:
        print("ERROR: no hostline is available!")
        sys.exit(1)
    # printing info with debug switch
    if args.debug:
        if os.name != "nt":
            run_rpc_debug(uptime=uptime, appid=computer.osinfoid, cpuappid=computer.cpuid, termappid=computer.terminalid,
                          packagesline=computer.packages, hostline=computer.host, hostappid=computer.hostappid)
        else:
            run_rpc_debug(uptime=uptime, appid=computer.osinfoid,
                          cpuappid=computer.cpuid)

    run: Run_rpc = Run_rpc()

    if computer.neofetchwin:
        # wandowz
        loops: Dict = {}
        loops_indexes: Dict = {}

        if not args.nodistro:
            loops["windows"] = (computer.osinfoid, windows)
            loops_indexes[len(loops_indexes)] = "windows"
        if not args.nohardware:
            loops["cycle1"] = (computer.cpuid, cycle1)
            loops_indexes[len(loops_indexes)] = "cycle1"

        run.set_loop(loops, loops_indexes, check_change, int(
            args.poll_rate) if args.poll_rate else 3)
        run.run_loop(computer)
    else:
        # loonix
        loops: Dict = {}
        loops_indexes: Dict = {}

        if not args.nodistro and computer.os != "macos":
            loops["cycle0"] = (computer.osinfoid, cycle0)
            loops_indexes[len(loops_indexes)] = "cycle0"
        if computer.os == "macos":
            loops["runmac"] = ("740822755376758944", runmac)
            loops_indexes[len(loops_indexes)] = "runmac"
        if not args.nohardware:
            loops["cycle1"] = (computer.cpuid, cycle1)
            loops_indexes[len(loops_indexes)] = "cycle1"
        if not args.noshell:
            loops["cycle2"] = (computer.terminalid, cycle2)
            loops_indexes[len(loops_indexes)] = "cycle2"
        if not args.nohost and computer.os != "macos":
            loops["cycle3"] = (computer.hostappid, cycle3)
            loops_indexes[len(loops_indexes)] = "cycle3"
        if args.pause_cycle:
            loops["pause"] = ("", pause)
            loops_indexes[len(loops_indexes)] = "pause"

        run.set_loop(loops, loops_indexes, check_change, int(
            args.poll_rate) if args.poll_rate else 3)
        run.run_loop(computer)


def runmac(run: Run_rpc, key: str, computer: Computer):
    from fetch_cord.testing import devicetype, product, bigicon, ver
    if args.debug:
        print("runmac")
        print("devicetype: %s" % devicetype)
        print("product %s" % product)
        print("bigicon: %s" % bigicon)
        print("ver: %s" % ver)
        print("uptime: %s" % uptime)
        # print("client_id: %s" % run.rpcs[key].client_id)

    run.try_update(key,
                   state=computer.packages,  # update state as packages
                   details=computer.kernel,  # update details as kernel
                   large_image=bigicon,  # set icon
                   large_text=computer.osinfo,  # set large icon text
                   small_image=devicetype,  # set small image icon
                   small_text=product,  # set small image text
                   start=start_time)
    if args.time:
        custom_time()
    elif args.nohost and args.nohardware and args.noshell:
        time.sleep(9999)
    else:
        time.sleep(30)
    run.try_clear(key)


def custom_time():
    ctime = int(args.time)
    time.sleep(ctime)


def cycle0(run: Run_rpc, key: str, computer: Computer):
    top_line = run.config["cycle_0"]["top_line"]
    if top_line == "kernel":
        top_line = computer.kernel
    else:
        top_line = computer.packages
    bottom_line = run.config["cycle_0"]["bottom_line"]
    if bottom_line == "kernel":
        bottom_line = computer.kernel
    else:
        bottom_line = computer.packages
    de_wm_icon = run.config["cycle_0"]["de_wm_icon"]
    if de_wm_icon == "on":
        de_wm_icon = computer.desktopid
    else:
        de_wm_icon = "off"
    if args.debug:
        print("cycle 0")
    run.try_update(key,
                   state=bottom_line,
                   details=top_line,
                   large_image="big",
                   large_text=computer.osinfo,
                   small_image=de_wm_icon,
                   small_text=computer.dewmid,
                   start=start_time)
    # if args.debug:
    #     print("appid: %s" % run.rpcs[key].client_id)
    config_time = run.config["cycle_0"]["time"]
    if args.time:
        custom_time()
    elif args.nohost and args.nohardware and args.noshell:
        time.sleep(9999)
    elif config_time:
        time.sleep(int(config_time))
    else:
        time.sleep(30)
    run.try_clear(key)


def cycle1(run: Run_rpc, key: str, computer: Computer):
    top_line = run.config["cycle_1"]["top_line"]
    if top_line == "gpu":
        top_line = computer.gpu
    elif top_line == "cpu":
        top_line = computer.cpu
    elif top_line == "mem":
        top_line = computer.memory
    elif top_line == "disk":
        top_line = computer.disks
    bottom_line = run.config["cycle_1"]["bottom_line"]
    if bottom_line == "gpu":
        bottom_line = computer.gpu
    elif bottom_line == "cpu":
        bottom_line = computer.cpu
    elif bottom_line == "mem":
        bottom_line = computer.memory
    elif bottom_line == "disk":
        bottom_line = computer.disks
    gpu_icon = run.config["cycle_1"]["gpu_icon"]
    if gpu_icon == "on":
        gpu_icon = computer.gpuid
    else:
        gpu_icon = "off"
    if args.debug:
        print("cycle 1")

    run.try_update(
        key,
        state=bottom_line,
        details=top_line,
        large_image="big",
        large_text=computer.cpu,
        small_image=gpu_icon,
        small_text=computer.gpu,
        start=start_time)
    # if args.debug:
    #     print("appid: %s" % client_id)
    config_time = run.config["cycle_1"]["time"]
    if args.time:
        custom_time()
    elif args.nodistro and args.noshell and args.nohost:
        time.sleep(9999)
    elif config_time:
        time.sleep(int(config_time))
    else:
        time.sleep(30)
    run.try_clear(key)


def cycle2(run: Run_rpc, key: str, computer: Computer):
    top_line = run.config["cycle_2"]["top_line"]
    if top_line == "font":
        top_line = computer.terminal
    elif top_line == "shell":
        top_line = computer.shellid
    elif top_line == "theme":
        top_line = computer.theme
    bottom_line = run.config["cycle_2"]["bottom_line"]
    if bottom_line == "font":
        bottom_line = computer.terminal
    elif bottom_line == "shell":
        bottom_line = computer.shell
    elif bottom_line == "theme":
        bottom_line = computer.theme
    shell_icon = run.config["cycle_2"]["shell_icon"]
    if shell_icon == "on":
        shell_icon = computer.shellid
    else:
        shell_icon = "off"
    if args.debug:
        print("cycle 2")

    run.try_update(
        key,
        state=bottom_line,
        details=top_line,
        large_image="big",
        large_text=computer.terminal,
        small_image=shell_icon,
        small_text=computer.shell,
        start=start_time)
    # if args.debug:
    #     print("appid: %s" % client_id)

    config_time = run.config["cycle_2"]["time"]

    if args.time:
        custom_time()
    elif args.nodistro and args.nohardware and args.nohost:
        time.sleep(9999)
    elif config_time:
        time.sleep(int(config_time))
    else:
        time.sleep(30)
    run.try_clear(key)


def cycle3(run: Run_rpc, key: str, computer: Computer):
    # if not then forget it
    if computer.host != 'Host: N/A':
        top_line = run.config["cycle_3"]["top_line"]
        if top_line == "battery":
            top_line = computer.battery
        elif top_line == "host":
            top_line = computer.host
        elif top_line == "resolution":
            top_line = computer.resolution
        bottom_line = run.config["cycle_3"]["bottom_line"]
        if bottom_line == "resolution":
            bottom_line = computer.resolution
        elif bottom_line == "host":
            bottom_line = computer.host
        elif bottom_line == "battery":
            bottom_line = computer.battery
        lapordesk_icon = run.config["cycle_3"]["lapordesk_icon"]
        if lapordesk_icon == "on":
            lapordesk_icon = computer.lapordesk
        else:
            lapordesk_icon = "off"
        if args.debug:
            print("cycle 3")

        run.try_update(key,
                       state=computer.resolution,
                       details=computer.battery,
                       large_image="big",
                       large_text=computer.host,
                       small_image=lapordesk_icon,
                       small_text=computer.lapordesk,
                       start=start_time)
        # if args.debug:
        #     print("appid: %s" % client_id)
        config_time = run.config["cycle_3"]["time"]
        if args.time:
            custom_time()
        elif args.nodistro and args.nohardware and args.noshell:
            time.sleep(9999)
        elif config_time:
            time.sleep(int(config_time))
        else:
            time.sleep(30)
    # back from whence you came
    run.try_clear(key)


def pause():
    if args.debug:
        print("pause_cycle")
    if args.time:
        custom_time()
    else:
        time.sleep(30)


def windows(run: Run_rpc, key: str, computer: Computer):
    if args.debug:
        print("w_cycle 0")

    run.try_connect(key)
    run.try_update(key,
                   state=computer.osinfo,
                   details=computer.memory,
                   large_image="big",
                   large_text=computer.osinfo,
                   small_image=computer.motherboardid,
                   small_text=computer.motherboard,
                   start=start_time)
    # if args.debug:
    #     print("appid: %s" % client_id)
    if args.time:
        custom_time()
    elif args.nohardware:
        time.sleep(9999)
    else:
        time.sleep(30)
    run.try_clear(key)


def check_change(computer: Computer):
    computer.updateMap()
