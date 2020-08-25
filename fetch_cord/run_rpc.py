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
from fetch_cord.out import gpuinfo, sysosline, sysosid, memline, getcpuinfo, cpuinfo, run_debug, neofetch
if os.name != "nt":
    from fetch_cord.testing import desktopid, termappid, hostappid
    from fetch_cord.out import packagesline, termid, shellid, kernelline, shell_line, fontline, \
        dewmid, termline, lapordesk, hostline, resline, themeline, diskline, batteryline, \
        get_gpu, cpuline
elif os.name == "nt":
    from fetch_cord.out import moboline
    from fetch_cord.testing import moboid

uptime = psutil.boot_time()
args = parse_args()


def main():
    if os.name != "nt":
        if hostline == "" and args.nodistro and args.noshell and args.nohardware:
            print("ERROR: no hostline is available!")
            sys.exit(1)
    # printing info with debug switch
    if args.debug:
        print("----run_rpc----\n")
        print("uptime in epoch: %s" % uptime)
        print("cpuid: %s" % appid)
        print("cpuappid: %s" % cpuappid)
        if os.name != "nt":
            print("termappid: %s" % termappid)
            if hostline:
                print("hostappid: %s" % hostappid)
            print(packagesline[0])
    i = 0
    if os.name == "nt":
        wandowz(i)
    else:
        loonix(i, gpuinfo)

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


def runmac(client_id):
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


def cycle1(gpuinfo):
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
        i = 1
    else:
        loonix(cpuinfo, i)
    rpc_tryclear(RPC)


def pause():
    if args.debug:
        print("pause_cycle")
    if args.time:
        custom_time()
    else:
        time.sleep(30)


def w_cycle0():
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


def w_cycle1():
    if args.debug:
        print("w_cycle 1")
    client_id = cpuappid
    RPC = Presence(client_id)
    rpc_tryconnect(RPC)
    rpc_tryupdate(RPC,
               state=diskline,
               details=gpuinfo,
               large_image="big",
               large_text=cpuinfo,
               small_image=gpuid,
               small_text=gpuinfo,
               start=start_time)
    if args.debug:
        print("appid: %s" % client_id)
    if args.time:
        custom_time()
    elif args.nodistro:
        time.sleep(9999)
    else:
        time.sleep(30)
    rpc_tryclear(RPC)

def check_change(i, gpuinfo):
    neofetch()
    from fetch_cord.out import memline, diskline, batteryline, packagesline, cpuinfo, cpuline
    global memline, diskline, batteryline, packagesline, cpuinfo
    cpuinfo = getcpuinfo(cpuline)
    memline = memline[0]
    if batteryline:
        batteryline = '\n'.join(batteryline)
    else:
        batteryline = lapordesk
    if diskline:
        diskline = '\n'.join(diskline)
    else:
        diskline = cpuinfo
    i = 1
    get_gpuinfo = ""
    gpuinfo = get_gpu(get_gpuinfo, i)
    if os.name != "nt":
        return loonix(i, gpuinfo)
    else:
        return wandowz(i)

def loonix(i, gpuinfo):
    try:
        if i == 0:
            first_connect()
        while i < 3:
            if not args.nodistro and sysosid.lower() != "macos":
                cycle0()
            if not args.nohardware:
                cycle1(gpuinfo)
            if not args.noshell:
                cycle2()
            if not args.nohost and sysosid.lower() != "macos":
                cycle3()
            if sysosid.lower() == "macos":
                runmac()
            if args.pause_cycle:
                pause()
            i += 1
        if not args.nohardware or not args.nodistro or not args.nohost:
            i = 1
            check_change(i, gpuinfo)
        else:
            i = 1
            loonix(i, gpuinfo)
    except (KeyboardInterrupt, ConnectionResetError):
        if KeyboardInterrupt:
            print("Closing connection.")
            sys.exit(0)
        else:
            rpc_tryconnect(RPC)


def wandowz(i):
    try:
        if i == 0:
            first_connect()
        while i < 3:
            if not args.nodistro:
                w_cycle0()
            if not args.nohardware:
                w_cycle1()
            i += 1
        if not args.nohardware:
            i = 1
            check_change(i, gpuinfo)
        else:
            i = 1
            wandowz(i)
    except (KeyboardInterrupt, ConnectionResetError):
        if KeyboardInterrupt:
            print("Closing connection.")
            sys.exit(0)
        else:
            rpc_tryconnect(RPC)
