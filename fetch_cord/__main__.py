# from __future__ import annotations

from typing import Dict
import sys, os

from .run_rpc import Run_rpc
from .cycles import cycle0, cycle1, cycle2, cycle3, runmac, windows, pause
from .computer.Computer import Computer
from .args import parse_args
from .debugger import run_rpc_debug
from .update import update
from . import __init__ as __init__
from .resources import systemd_service


def main():
    args = parse_args()

    if args.update:
        update()
    if os.name != "nt" and sys.platform != "darwin":
        if args.install:
            systemd_service.install()
        if args.uninstall:
            systemd_service.uninstall()
        if args.enable:
            systemd_service.enable()
        if args.disable:
            systemd_service.disable()
        if args.start:
            systemd_service.start()
        if args.stop:
            systemd_service.stop()
        if args.status:
            systemd_service.status()
    if args.version:
        print("FetchCord version:", __init__.VERSION)
        sys.exit(0)
    if args.time:
        if int(args.time) < 15:
            print("ERROR: Invalid time set, must be > 15 seconds, cannot continue.")
            sys.exit(1)
        else:
            print("setting custom time %s seconds" % args.time)
    try:
        if args.help:
            sys.exit(0)
    except AttributeError:
        pass

    computer: Computer = Computer()

    if (
        not computer.neofetchwin
        and computer.host == "Host: N/A"
        and args.nodistro
        and args.noshell
        and args.nohardware
    ):
        print("ERROR: no hostline is available!")
        sys.exit(1)
    # printing info with debug switch
    if args.debug:
        run_rpc_debug(computer)

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

        run.set_loop(
            loops,
            loops_indexes,
            computer.updateMap,
            int(args.poll_rate) if args.poll_rate else 3,
        )
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

        run.set_loop(
            loops,
            loops_indexes,
            computer.updateMap,
            int(args.poll_rate) if args.poll_rate else 3,
        )
        run.run_loop(computer)


if __name__ == "__main__":
    main()