# Import cool new rpc module that gives us more control and gets rid of headaches :)
from pypresence import Presence, exceptions
import time
import sys
import os
import psutil
# import info about system
from fetch_cord.args import parse_args
from fetch_cord.testing import gpuid, appid, cpuappid
from fetch_cord.out import gpuinfo, sysosline, sysosid, cpuinfo
if os.name != "nt":
    from fetch_cord.testing import desktopid, termappid, hostappid
    from fetch_cord.out import packagesline, termid, shellid, kernelline, shell_line, termfontline, \
        dewmid, termline, lapordesk, hostline, resline
elif os.name == "nt":
    from fetch_cord.out import moboline, memline
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
        print("run-rpc")
        print(uptime)
        print(appid)
        print(gpuid)
        if os.name != "nt":
            print(packagesline[0])
    if os.name == "nt":
        wandowz()
    else:
        loonix()


print("Connecting")
time.sleep(5)
# discord uses unix time to interpret time for rich presnse, this is uptime in unix time
start_time = float(uptime)
print("RPC connection successful.")


def rpc_tryconnect():
    while True:
        try:
            RPC.connect()
            break
        except ConnectionRefusedError:
            print("RPC connection refused (is Discord open?); trying again in 30 seconds")
            time.sleep(30)


def rpc_tryclear():
    try:
        RPC.clear(pid=os.getpid())
    except exceptions.InvalidID:
        pass


def rpc_tryupdate(state, details, large_image, large_text, small_image, small_text, start):
    try:
        RPC.update(state=state, details=details, large_image=large_image,
                    large_text=large_text, small_image=small_image, small_text=small_text,
                    start=start)
    # ConnectionResetError is here to avoid crashing if Discord is still just starting
    except (ConnectionResetError, exceptions.InvalidID):
        pass


def runmac():
    global RPC
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
    rpc_tryconnect()
    rpc_tryupdate(state=packagesline[0],  # update state as packages
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


def custom_time():
    ctime = int(args.time)
    time.sleep(ctime)


# cycle


def cycle0():
    global RPC
    if args.debug:
        print("cycle 0")
    client_id = appid
    RPC = Presence(client_id)
    rpc_tryconnect()
    rpc_tryupdate(state=packagesline[0],
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


# cycle


def cycle1():
    global RPC
    if args.debug:
        print("cycle 1")
    client_id = cpuappid
    RPC = Presence(client_id)
    rpc_tryconnect()
    rpc_tryupdate(state=cpuinfo,
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
    elif args.nodistro and args.noshell and args.nohost:
        time.sleep(9999)
    else:
        time.sleep(30)


# cycle


def cycle2():
    global RPC
    if args.debug:
        print("cycle 2")
    client_id = termappid
    RPC = Presence(client_id)
    rpc_tryconnect()
    rpc_tryupdate(state=shell_line[0],
               details=termfontline,
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


def cycle3():
    # if not then forget it
    if hostline:
        global RPC
        if args.debug:
            print("cycle 3")
        client_id = hostappid
        RPC = Presence(client_id)
        rpc_tryconnect()
        rpc_tryupdate(state=resline,
                details=hostline[0],
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
        loonix()


def w_cycle0():
    global RPC
    if args.debug:
        print("cycle 0")
    client_id = appid
    RPC = Presence(client_id)
    rpc_tryconnect()
    rpc_tryupdate(state=sysosline[0],
               details=memline[0],
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


def w_cycle1():
    global RPC
    if args.debug:
        print("cycle 1")
    client_id = cpuappid
    RPC = Presence(client_id)
    rpc_tryconnect()
    rpc_tryupdate(state=cpuinfo,
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



def loonix():
    try:
        while True:
            if not args.nodistro and sysosid.lower() != "macos":
                cycle0()
                rpc_tryclear()
            if not args.nohardware:
                cycle1()
                rpc_tryclear()
            if not args.noshell:
                cycle2()
                rpc_tryclear()
            if not args.nohost and sysosid.lower() != "macos":
                cycle3()
                rpc_tryclear()
            if sysosid.lower() == "macos":
                runmac()
                rpc_tryclear()
    except KeyboardInterrupt:
        print("Closing connection.")
        sys.exit(0)


def wandowz():
    try:
        while True:
            if not args.nodistro:
                w_cycle0()
                rpc_tryclear()
            if not args.nohardware:
                w_cycle1()
                rpc_tryclear()
    except KeyboardInterrupt:
        print("Closing connection.")
        sys.exit(0)
