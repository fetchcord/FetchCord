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
            if batteryline != lapordesk:
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

