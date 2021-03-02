#from __future__ import annotations

from typing import List

from .computer.Computer import Computer
from .computer.cpu.Cpu_interface import Cpu_interface


def run_debug(computer: Computer):
    print("----out.py----\n")
    print("----DE/WM----")
    if computer.os != "windows":
        print("deid: %s" % computer.deid)
        print("wmid: %s" % computer.wmid)
        try:
            print("wmline item 0: %s" % computer.wm)
        except IndexError:
            pass
        print("\n----TERMINAL----\n")
        print("fontline: %s" % computer.font)
        print("termid: %s" % computer.terminalid)
        print("termline item 0: %s" % computer.terminal)
        print("themeline: %s" % computer.theme)
        if computer.host != "Host: N/A":
            print("\n----HOST INFO----\n")
            print("hostline: %s" % computer.host)
            if computer.battery != computer.host:
                print("batteryline: %s" % computer.battery)
            print("resline: %s" % computer.resolution)
    print("\n----GPU INFO----\n")
    print("gpuinfo: %s" % computer.gpu)
    print("gpuvendor: %s" % computer.gpuid)
    print("\n----CPU INFO----\n")
    cpu: List[Cpu_interface] = computer.get_component("CPU:")
    if cpu:
        print("cpuvendor: %s" % cpu[0].vendor)
        print("cpumodel: %s" % cpu[0].model)
        print("cpuinfo: %s" % cpu[0].info)
    print("cpuline item 0: %s" % computer.cpu)
    print("memline: %s" % computer.memory)
    print("\n----OS INFO----\n")
    print("sysosline: %s" % computer.osinfo)
    print("sysosid: %s" % computer.osinfoid)
    print("diskline: %s" % computer.disks)
    if computer.os != "windows":
        print("packagesline item 0: %s" % computer.packages)


def test_debug(computer: Computer):
    print("\n----testing.py----")
    if computer.os != "windows":
        print("----DE/WM----\n")
        print("deid: %s" % computer.deid)
        print("wmid: %s" % computer.wmid)
        print("\n----TERMINAL/SHELL----\n")
        print("termid: %s" % computer.terminalid)
        print("shellid: %s" % computer.shellid)
        print("\n----HOST INFO----\n")
        print("hostid: %s" % computer.hostid)
    else:
        print("moboid: %s" % computer.motherboardid)
        print("moboline: %s" % computer.motherboard)
    print("\n----GPU INFO----\n")
    print("gpuvendor: %s" % computer.gpuid)
    print("\n----CPU INFO----\n")
    cpu = computer.get_component("CPU:")
    if cpu:
        print("cpumodel: %s\n" % cpu[0].model)


def run_rpc_debug(computer: Computer):
    print("----run_rpc----\n")
    print("uptime in epoch: %s" % computer.uptime)
    print("cpuid: %s" % computer.osinfoid)
    print("cpuappid: %s" % computer.cpuid)
    if computer.os != "windows":
        print("termappid: %s" % computer.terminalid)
        if computer.host != "Host: N/A":
            print("hostappid: %s" % computer.hostappid)
        print(computer.packages)

    run_debug(computer)
    test_debug(computer)