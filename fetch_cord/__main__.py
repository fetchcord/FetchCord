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

  if os.name != "nt" and sys.platform != "darwin" and args.update:
    update()
  elif args.install:
    systemd_service.install()
  elif args.uninstall:
    systemd_service.uninstall()
  elif args.enable:
    systemd_service.enable()
  elif args.disable:
    systemd_service.disable()
  elif args.start:
    systemd_service.start()
  elif args.stop:
    systemd_service.stop()
  elif args.status:
    systemd_service.status()
  elif args.version:
    print("FetchCord version:", __init__.VERSION)
    sys.exit(0)
  if args.time and float(args.time) < 15:
    print("ERROR: Invalid time set, must be > 15 seconds, please try again with a different time setting!")
    sys.exit(1)
  elif args.time and float(args.time) >= 15 != "":
    print("setting custom time %s seconds" % args.time)
  elif args.help:
    sys.exit(0)
  
  computer: Computer = Computer()

  if (not computer.neofetchwin and computer.host == "Host: N/A" and computer.motherboard == "Motherboard: N/A" and args.nodistro and args.noshell and args.nohardware):
    print("ERROR: no hostline is available!")
    sys.exit(1)
  # printing info with debug switch
  if args.debug:
    run_rpc_debug(computer)

  run: Run_rpc = Run_rpc()

  if os.WIFSTOPPED or os.WSTOPSIG:
    print("Connection Error: Please connect to the internet to use FetchCord!")
  elif computer.neofetchwin:
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
      loops["cycle3"] = (computer.motherboardappid, cycle3)
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
