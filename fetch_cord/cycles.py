#from __future__ import annotations

import time
from typing import Dict

from .computer.Computer import Computer
from .run_rpc import Run_rpc
from .args import parse_args

args = parse_args()


class Cycles:
    config: Dict[str, str]

    def __init__(self, config: Dict[str, str]):
        self.config = config


def pause(run: Run_rpc, key: str, computer: Computer):
    if args.debug:
        print("pause_cycle")
    if args.time:
        time.sleep(int(args.time))
    else:
        time.sleep(30)


def windows(run: Run_rpc, key: str, computer: Computer):
    if args.debug:
        print("w_cycle 0")

    run.try_update(
        key,
        state=computer.osinfo,
        details=computer.memory,
        large_image="big",
        large_text=computer.osinfo,
        small_image=computer.motherboardid,
        small_text=computer.motherboard,
        start=computer.uptime,
    )

    if args.time:
        time.sleep(int(args.time))
    elif args.nohardware:
        time.sleep(9999)
    else:
        time.sleep(30)
    run.try_clear(key)


def runmac(run: Run_rpc, key: str, computer: Computer):
    if args.debug:
        print("runmac")
        print("devicetype: %s" % computer.devicetype)
        print("product %s" % computer.product)
        print("bigicon: %s" % computer.bigicon)
        print("ver: %s" % computer.version)
        print("uptime: %s" % computer.uptime)

    run.try_update(
        key,
        state=computer.packages,  # update state as packages
        details=computer.kernel,  # update details as kernel
        large_image=computer.bigicon,  # set icon
        large_text=computer.osinfo,  # set large icon text
        small_image=computer.devicetype,  # set small image icon
        small_text=computer.product,  # set small image text
        start=computer.uptime,
    )
    if args.time:
        time.sleep(int(args.time))
    elif args.nohost and args.nohardware and args.noshell:
        time.sleep(9999)
    else:
        time.sleep(30)
    run.try_clear(key)


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

    run.try_update(
        key,
        state=bottom_line,
        details=top_line,
        large_image="big",
        large_text=computer.osinfo,
        small_image=de_wm_icon,
        small_text=computer.dewmid,
        start=computer.uptime,
    )
    if args.debug:
        print("appid: %s" % computer.osinfoid)
    config_time = run.config["cycle_0"]["time"]
    if args.time:
        time.sleep(int(args.time))
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
        start=computer.uptime,
    )
    if args.debug:
        print("appid: %s" % computer.cpuid)
    config_time = run.config["cycle_1"]["time"]
    if args.time:
        time.sleep(int(args.time))
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
        start=computer.uptime,
    )
    if args.debug:
        print("appid: %s" % computer.osinfoid)

    config_time = run.config["cycle_2"]["time"]

    if args.time:
        time.sleep(int(args.time))
    elif args.nodistro and args.nohardware and args.nohost:
        time.sleep(9999)
    elif config_time:
        time.sleep(int(config_time))
    else:
        time.sleep(30)
    run.try_clear(key)


def cycle3(run: Run_rpc, key: str, computer: Computer):
    # if not then forget it
    if computer.host != "Host: N/A":
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
        run.try_update(
            key,
            state=computer.resolution,
            details=computer.battery,
            large_image="big",
            large_text=computer.host,
            small_image=lapordesk_icon,
            small_text=computer.lapordesk,
            start=computer.uptime,
        )
        if args.debug:
            print("appid: %s" % computer.hostappid)
        config_time = run.config["cycle_3"]["time"]
        if args.time:
            time.sleep(int(args.time))
        elif args.nodistro and args.nohardware and args.noshell:
            time.sleep(9999)
        elif config_time:
            time.sleep(int(config_time))
        else:
            time.sleep(30)
    # back from whence you came
    run.try_clear(key)
