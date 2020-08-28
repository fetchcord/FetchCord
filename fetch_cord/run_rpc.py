# Import cool new rpc module that gives us more control and gets rid of headaches :)
from pypresence import Presence, exceptions
import time
import sys
import os
import psutil
# import info about system
from fetch_cord.args import parse_args
from fetch_cord.bash import BashError, exec_bash
from fetch_cord.testing import gpuid, cpuappid, appid
from fetch_cord.debugger import run_rpc_debug
from fetch_cord.out import gpuinfo, sysosline, sysosid, memline, cpuinfo, \
        neofetch, diskline, neofetchwin, baseinfo
if os.name != "nt":
    from fetch_cord.testing import desktopid, termappid, hostappid, shellid
    from fetch_cord.out import packagesline, kernelline, shell_line, fontline, \
        termline, lapordesk, hostline, resline, themeline, batteryline, \
        gpuinfo, dewmid
elif os.name == "nt":
    from fetch_cord.out import moboline, check_neofetchwin
    from fetch_cord.testing import moboid


uptime = psutil.boot_time()
args = parse_args()

if os.name == "nt":
    neofetchwin = check_neofetchwin()
else:
    neofetchwin = False

def main():
    if os.name != "nt" and not hostline and args.nodistro and args.noshell and args.nohardware:
        print("ERROR: no hostline is available!")
        sys.exit(1)
    # printing info with debug switch
    if args.debug:
        if baseinfo:
            run_rpc_debug(uptime=uptime, appid=appid, cpuappid=cpuappid, termappid=termappid, packagesline=packagesline, hostline=hostline, hostappid=hostappid)
        else:
            run_rpc_debug(uptime=uptime, appid=appid, cpuappid=cpuappid)
    loop = 0
    if neofetchwin:
        wandowz(loop)
    else:
        loonix(loop)

def first_connect():
    try:
        client_id = appid
        RPC = Presence(client_id)
        RPC.connect()
        print("RPC Connection Successful.")
    except ConnectionRefusedError:
        rpc_tryconnect(RPC)

print("Connecting")
try:
    time.sleep(5)
except KeyboardInterrupt:
    print("Stopping connection.")
    sys.exit(0)
# discord uses unix time to interpret time for rich presnse, this is uptime in unix time
start_time = float(uptime)


def rpc_tryconnect(RPC):
    while True:
        try:
            RPC.connect()
            break
        except ConnectionRefusedError:
            print("RPC connection refused (is Discord open?); trying again in 30 seconds")
            time.sleep(30)



def rpc_tryclear(RPC):
    try:
        RPC.clear(pid=os.getpid())
    except exceptions.InvalidID:
        pass


def rpc_tryupdate(RPC, state, details, large_image, large_text, small_image, small_text, start):
    try:
        RPC.update(state=state, details=details, large_image=large_image,
                    large_text=large_text, small_image=small_image, small_text=small_text,
                    start=start)
    # ConnectionResetError is here to avoid crashing if Discord is still just starting
    except (ConnectionResetError, exceptions.InvalidID):
        pass


def runmac():
    from fetch_cord.testing import devicetype, product, bigicon, ver
    client_id = '740822755376758944'  # macos appid for discord rpc
    if args.debug:
        print("runmac")
        print("devicetype: %s" % devicetype)
        print("product %s" % product)
        print("bigicon: %s" % bigicon)
        print("ver: %s" % ver)
        print("uptime: %s" % uptime)
        print("client_id: %s" % client_id)
    RPC = Presence(client_id)
    rpc_tryconnect(RPC)
    rpc_tryupdate(RPC,
                state=packagesline[0],  # update state as packages
                details=kernelline[0],  # update details as kernel
                large_image=bigicon,  # set icon
                large_text=sysosline[0],  # set large icon text
                small_image=devicetype,  # set small image icon
                small_text=product,  # set small image text
                start=start_time)
    if args.time:
        custom_time()
    elif args.nohost and args.nohardware and args.noshell:
        time.sleep(9999)
    else:
        time.sleep(30)
    rpc_tryclear(RPC)

def custom_time():
    ctime = int(args.time)
    time.sleep(ctime)


# cycle


def cycle0():
    if args.debug:
        print("cycle 0")
    client_id = appid
    RPC = Presence(client_id)
    rpc_tryconnect(RPC)
    rpc_tryupdate(RPC,
               state=packagesline[0],
               details=kernelline[0],
               large_image="big",
               large_text=sysosline[0],
               small_image=desktopid,
               small_text=dewmid,
               start=start_time)
    if args.debug:
        print("appid: %s" % client_id)

    if args.time:
        custom_time()
    elif args.nohost and args.nohardware and args.noshell:
        time.sleep(9999)
    else:
        time.sleep(30)
    rpc_tryclear(RPC)


# cycle


def cycle1():
    if args.debug:
        print("cycle 1")
    client_id = cpuappid
    RPC = Presence(client_id)
    rpc_tryconnect(RPC)
    rpc_tryupdate(RPC,
               state=diskline,
               details=memline,
               large_image="big",
               large_text=cpuinfo,
               small_image=gpuid,
               small_text=gpuinfo,
               start=start_time)
    if args.debug:
        print("appid: %s" % client_id)
    if args.time:
        custom_time()
    elif args.nodistro and args.noshell and args.nohost:
        time.sleep(9999)
    else:
        time.sleep(30)
    rpc_tryclear(RPC)


# cycle


def cycle2():
    if args.debug:
        print("cycle 2")
    client_id = termappid
    RPC = Presence(client_id)
    rpc_tryconnect(RPC)
    rpc_tryupdate(RPC,
               state=themeline,
               details=fontline,
               large_image="big",
               large_text=termline[0],
               small_image=shellid,
               small_text=shell_line[0],
               start=start_time)
    if args.debug:
        print("appid: %s" % client_id)
    if args.time:
        custom_time()
    elif args.nodistro and args.nohardware and args.nohost:
        time.sleep(9999)
    else:
        time.sleep(30)
    rpc_tryclear(RPC)


def cycle3():
    # if not then forget it
    if hostline:
        if args.debug:
            print("cycle 3")
        client_id = hostappid
        RPC = Presence(client_id)
        rpc_tryconnect(RPC)
        rpc_tryupdate(RPC,
                state=resline,
                details=batteryline,
                large_image="big",
                large_text=hostline[0],
                small_image=lapordesk,
                small_text=lapordesk,
                start=start_time)
        if args.debug:
            print("appid: %s" % client_id)
        if args.time:
            custom_time()
        elif args.nodistro and args.nohardware and args.noshell:
            time.sleep(9999)
        else:
            time.sleep(30)
    # back from whence you came
    else:
        loop = 1
        loonix(loop)
    rpc_tryclear(RPC)


def pause():
    if args.debug:
        print("pause_cycle")
    if args.time:
        custom_time()
    else:
        time.sleep(30)


def windows():
    if args.debug:
        print("w_cycle 0")
    client_id = appid
    RPC = Presence(client_id)
    rpc_tryconnect(RPC)
    rpc_tryupdate(RPC,
               state=sysosline[0],
               details=memline,
               large_image="big",
               large_text=sysosline[0],
               small_image=moboid,
               small_text=moboline[0],
               start=start_time)
    if args.debug:
        print("appid: %s" % client_id)
    if args.time:
        custom_time()
    elif args.nohardware:
        time.sleep(9999)
    else:
        time.sleep(30)
    rpc_tryclear(RPC)


def check_change(loop):

    neofetch(loop)

    from fetch_cord.out import diskline, nvidiagpuline, \
            memline, cpuline, gpuinfo
    from fetch_cord.checks import get_cpuinfo, check_diskline, check_batteryline, check_memline
    if os.name != "nt" or baseinfo:
        from fetch_cord.checks import check_batteryline
        from fetch_cord.out import lapordesk, batteryline, packagesline, check_batteryline, get_gpuinfo, cirrusgpuline, virtiogpuline, vmwaregpuline, intelgpuline, amdgpuline, primeoffload, sysosid, amdgpurenderlist

    global packagesline, cpuinfo, gpuinfo, memline, diskline, batteryline

    memline = check_memline(memline)
    cpuinfo = get_cpuinfo(cpuline, baseinfo)
    diskline = check_diskline(diskline, cpuinfo)
    if os.name != "nt" or baseinfo:
        batteryline = check_batteryline(batteryline, hostline)
        packagesline = packagesline

    if os.name != "nt" or baseinfo and nvidiagpuline and sysosid.lower() != "macos":
        from fetch_cord.out import gpuinfo
        gpuinfo = get_gpuinfo(cirrusgpuline, vmwaregpuline, virtiogpuline, amdgpuline, nvidiagpuline,\
        intelgpuline, primeoffload, amdgpurenderlist,sysosid, loop)

    loop = 1

    if not neofetchwin:
        return loonix(loop)
    else:
        return wandowz(loop)

def loonix(loop):
    try:
        if loop == 0:
            first_connect()
        while loop < 3:
            if not args.nodistro and sysosid.lower() != "macos":
                cycle0()
            if not args.nohardware:
                cycle1()
            if not args.noshell:
                cycle2()
            if not args.nohost and sysosid.lower() != "macos":
                cycle3()
            if sysosid.lower() == "macos":
                runmac()
            if args.pause_cycle:
                pause()
            loop += 1
        if not args.nohardware or not args.nodistro or not args.nohost:
            loop = 1
            check_change(loop)
        else:
            loop = 1
            loonix(loop, gpuinfo)
    except (KeyboardInterrupt, ConnectionResetError):
        if KeyboardInterrupt:
            print("Closing connection.")
            sys.exit(0)
        else:
            rpc_tryconnect(RPC)


def wandowz(loop):
    try:
        if loop == 0:
            first_connect()
        while loop < 3:
            if not args.nodistro:
                windows()
            if not args.nohardware:
                cycle1()
            loop += 1
        if not args.nohardware:
            loop = 1
            check_change(loop)
        else:
            loop = 1
            wandowz(loop)
    except (KeyboardInterrupt, ConnectionResetError):
        if KeyboardInterrupt:
            print("Closing connection.")
            sys.exit(0)
        else:
            rpc_tryconnect(RPC)
