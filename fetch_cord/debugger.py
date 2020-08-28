import os
import sys

def run_debug():
    from fetch_cord.out import gpuinfo, cpuvendor, cpumodel, cpuinfo, cpuline, memline,\
            sysosid, sysosline, gpuvendor, diskline
    if os.name != "nt":
        from fetch_cord.out import deid, wmid, wmline, hostline, fontline, lapordesk, batteryline, \
            termid, packagesline, termline, themeline

    print("----out.py----\n")
    print("----DE/WM----")
    if os.name != "nt":
        print("deid: %s" % deid)
        print("wmid: %s" % wmid)
        try:
            print("wmline item 0: %s" % wmline[0])
        except IndexError:
            pass
        print("\n----TERMINAL----\n")
        print("fontline: %s" % fontline)
        print("termid: %s" % termid)
        print("termline item 0: %s" % termline[0])
        print("themeline: %s" % themeline)
        if hostline:
            print("\n----HOST INFO----\n")
            print("hostline: %s" % hostline)
            if batteryline != hostline[0]:
                print("batteryline: %s" % batteryline)
    print("\n----GPU INFO----\n")
    print("gpuinfo: %s" % gpuinfo)
    print("gpuvendor: %s" % gpuvendor)
    print("\n----CPU INFO----\n")
    print("cpuvendor: %s" % cpuvendor)
    print("cpumodel: %s" % cpumodel)
    print("cpuinfo: %s" % cpuinfo)
    print("cpuline item 0: %s" % cpuline[0])
    print("memline: %s" % memline)
    print("\n----OS INFO----\n")
    print("sysosline: %s" % sysosline)
    print("sysosid: %s" % sysosid)
    if diskline != cpuinfo:
        print("diskline: %s" % diskline)
    if os.name != "nt":
        print("packagesline item 0: %s" % packagesline[0])


def test_debug(gpuvendor, cpumodel, hostid, moboid, moboline = "N/A", deid = "N/A", wmid = "N/A", termid = "N/A", shellid = "N/A"):
    print("\n----testing.py----")
    if os.name != "nt":
        print("----DE/WM----\n")
        print("deid: %s" % deid)
        print("wmid: %s" % wmid)
        print("\n----TERMINAL/SHELL----\n")
        print("termid: %s" % termid)
        print("shellid: %s" % shellid)
        print("\n----HOST INFO----\n")
        print("hostid: %s" % hostid)
    elif os.name == "nt":
        print("moboid: %s" % moboid)
        print("moboline: %s" % moboline)
    print("\n----GPU INFO----\n")
    print("gpuvendor: %s" % gpuvendor)
    print("\n----CPU INFO----\n")
    print("cpumodel: %s\n" % cpumodel)

def run_rpc_debug(uptime, appid, cpuappid, hostappid = "N/A", hostline = "N/A",packagesline = "N/A", termappid="N/A"):
        print("----run_rpc----\n")
        print("uptime in epoch: %s" % uptime)
        print("cpuid: %s" % appid)
        print("cpuappid: %s" % cpuappid)
        if os.name != "nt":
            print("termappid: %s" % termappid)
            if hostline:
                print("hostappid: %s" % hostappid)
            print(packagesline[0])

