# Import cool new rpc module that gives us more control and gets rid of headaches :)
from pypresence import Presence, exceptions
import time
import sys
import os
import psutil
# import info about system
from fetch_cord.args import parse_args
from fetch_cord.config import ConfigError, load_config
from fetch_cord.bash import BashError, exec_bash
from fetch_cord.testing import gpuid, cpuappid, appid, desktopid, termappid, hostappid, shellid, moboid
from fetch_cord.debugger import run_rpc_debug
from fetch_cord.out import sysosline, sysosid, memline, cpuinfo, neofetch, diskline, hostline,\
        gpuinfo, packagesline, kernelline,shell_line, fontline, termline, lapordesk, resline, \
        themeline, batteryline, dewmid, moboline, neofetchwin


uptime = psutil.boot_time()
args = parse_args()


def main():
    if not neofetchwin and not hostline and args.nodistro and args.noshell and args.nohardware:
        print("ERROR: no hostline is available!")
        sys.exit(1)
    # printing info with debug switch
    if args.debug:
        if os.name != "nt":
            run_rpc_debug(uptime=uptime, appid=appid, cpuappid=cpuappid, termappid=termappid, packagesline=packagesline, hostline=hostline, hostappid=hostappid)
        else:
            run_rpc_debug(uptime=uptime, appid=appid, cpuappid=cpuappid)
    loop = 0
    if neofetchwin:
        config = get_config()
        wandowz(loop, config)
    else:
        config = get_config()
        loonix(config, loop, gpuinfo, memline, cpuinfo, diskline, batteryline, packagesline)

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
                state=packagesline,  # update state as packages
                details=kernelline,  # update details as kernel
                large_image=bigicon,  # set icon
                large_text=sysosline,  # set large icon text
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

def get_config():
    try:
        config = load_config()
    except ConfigError as e:
        print("Error loading config file, using default values." % str(e))
    return config

def custom_time():
    ctime = int(args.time)
    time.sleep(ctime)


# cycle


def cycle0(config, packagesline):
    top_line = config["cycle_0"]["top_line"]
    if top_line == "kernel":
        top_line = kernelline
    else:
        top_line = packagesline
    bottom_line = config["cycle_0"]["bottom_line"]
    if bottom_line == "kernel":
        bottom_line = kernelline
    else:
        bottom_line = packagesline
    if args.debug:
        print("cycle 0")
    client_id = appid
    RPC = Presence(client_id)
    rpc_tryconnect(RPC)
    rpc_tryupdate(RPC,
               state=bottom_line,
               details=top_line,
               large_image="big",
               large_text=sysosline,
               small_image=desktopid,
               small_text=dewmid,
               start=start_time)
    if args.debug:
        print("appid: %s" % client_id)
    config_time = config["cycle_0"]["time"]
    if args.time:
        custom_time()
    elif args.nohost and args.nohardware and args.noshell:
        time.sleep(9999)
    elif config_time:
        time.sleep(int(config_time))
    else:
        time.sleep(30)
    rpc_tryclear(RPC)


# cycle


def cycle1(config, gpuinfo, cpuinfo, memline, diskline):
    top_line = config["cycle_1"]["top_line"]
    if top_line == "gpu":
        top_line = gpuinfo
    else:
        top_line = memline
    bottom_line = config["cycle_1"]["bottom_line"]
    if bottom_line == "gpu":
        bottom_line = gpuinfo
    else:
        bottom_line = memline
    if args.debug:
        print("cycle 1")
    client_id = cpuappid
    RPC = Presence(client_id)
    rpc_tryconnect(RPC)
    rpc_tryupdate(RPC,
               state=bottom_line,
               details=top_line,
               large_image="big",
               large_text=cpuinfo,
               small_image=gpuid,
               small_text=gpuinfo,
               start=start_time)
    if args.debug:
        print("appid: %s" % client_id)
    config_time = config["cycle_1"]["time"]
    if args.time:
        custom_time()
    elif args.nodistro and args.noshell and args.nohost:
        time.sleep(9999)
    elif config_time:
        time.sleep(int(config_time))
    else:
        time.sleep(30)
    rpc_tryclear(RPC)


# cycle


def cycle2(config):
    top_line = config["cycle_2"]["top_line"]
    if top_line == "termfont":
        top_line = termline
    else:
        top_line = shellid
    bottom_line = config["cycle_2"]["bottom_line"]
    if bottom_line == "termfont":
        bottom_line = termline
    else:
        bottom_line = shell_line
    if args.debug:
        print("cycle 2")
    client_id = termappid
    RPC = Presence(client_id)
    rpc_tryconnect(RPC)
    rpc_tryupdate(RPC,
               state=bottom_line,
               details=top_line,
               large_image="big",
               large_text=termline,
               small_image=shellid,
               small_text=shell_line,
               start=start_time)
    if args.debug:
        print("appid: %s" % client_id)

    config_time = config["cycle_2"]["time"]

    if args.time:
        custom_time()
    elif args.nodistro and args.nohardware and args.nohost:
        time.sleep(9999)
    elif config_time:
        time.sleep(int(config_time))
    else:
        time.sleep(30)
    rpc_tryclear(RPC)


def cycle3(config, batteryline):
    # if not then forget it
    if hostline:
        top_line = config["cycle_3"]["top_line"]
        if top_line == "batteryline":
            top_line = batteryline
        else:
            top_line = hostline
        bottom_line = config["cycle_3"]["bottom_line"]
        if bottom_line == "resline":
            bottom_line = resline
        else:
            bottom_line = lapordesk
        if args.debug:
            print("cycle 3")
        client_id = hostappid
        RPC = Presence(client_id)
        rpc_tryconnect(RPC)
        rpc_tryupdate(RPC,
                state=resline,
                details=batteryline,
                large_image="big",
                large_text=hostline,
                small_image=lapordesk,
                small_text=lapordesk,
                start=start_time)
        if args.debug:
            print("appid: %s" % client_id)
        config_time = config["cycle_3"]["time"]
        if args.time:
            custom_time()
        elif args.nodistro and args.nohardware and args.noshell:
            time.sleep(9999)
        elif config_time:
            time.sleep(int(config_time))
        else:
            time.sleep(30)
    # back from whence you came
    else:
        loop = 1
        loonix(config, loop, gpuinfo, memline, cpuinfo, diskline, batteryline, packagesline)
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
               state=sysosline,
               details=memline,
               large_image="big",
               large_text=sysosline,
               small_image=moboid,
               small_text=moboline,
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


def check_change(config, loop):

    cpuline, gpuline, termline, fontline, wmline, radgpuline, \
            shell_line, kernelline, sysosline, moboline, neofetchwin,\
            deline, batteryline, resline, themeline, hostline, memline, packagesline, diskline = neofetch(loop)


    from fetch_cord.checks import get_cpuinfo, get_gpuinfo
    from fetch_cord.out import primeoffload, sysosid, amdgpurenderlist, laptop, primeoffload

    memline = ''.join(memline)
    packagesline = ''.join(packagesline)
    batteryline = ''.join(batteryline)
    diskline = '\n'.join(diskline)

    cpuinfo = get_cpuinfo(cpuline)
    for line in range(len(gpuline)):
        if sysosid.lower() != "macos" and "NVIDIA" in gpuline[line]:
            gpuinfo = get_gpuinfo(primeoffload, gpuline, laptop, sysosid, amdgpurenderlist)

    loop = 1

    if os.name != "nt":
        return loonix(config, loop, gpuinfo, memline,  cpuinfo, diskline, batteryline, packagesline)
    else:
        return wandowz(loop, config)

def loonix(config, loop, gpuinfo, memline, cpuinfo, diskline, batteryline, pacakgesline):
    try:
        if args.poll_rate:
            rate = int(args.poll_rate)
        else:
            rate = 3
        if loop == 0:
            first_connect()
        while loop < rate:
            if not args.nodistro and sysosid.lower() != "macos":
                cycle0(config, pacakgesline)
            if sysosid.lower() == "macos":
                runmac()
            if not args.nohardware:
                cycle1(config, gpuinfo, cpuinfo, memline, diskline)
            if not args.noshell:
                cycle2(config)
            if not args.nohost and sysosid.lower() != "macos":
                cycle3(config, batteryline)
            if args.pause_cycle:
                pause()
            loop += 1
        if not args.nohardware or not args.nodistro or not args.nohost:
            loop = 1
            check_change(config, loop)
        else:
            loop = 1
            loonix(loop)
    except (KeyboardInterrupt, ConnectionResetError):
        if KeyboardInterrupt:
            print("Closing connection.")
            sys.exit(0)
        elif ConnectionResetError:
            rpc_tryconnect(RPC)


def wandowz(loop, config):
    try:
        if loop == 0:
            first_connect()
        while loop < 3:
            if not args.nodistro:
                windows()
            if not args.nohardware:
                cycle1(config, gpuinfo, cpuinfo, memline, diskline)
        if not args.nohardware:
            loop = 1
            check_change(loop)
        else:
            loop = 1
            wandowz(loop, config)
    except (KeyboardInterrupt, ConnectionResetError):
        if KeyboardInterrupt:
            print("Closing connection.")
            sys.exit(0)
        if ConnectionResetError:
            rpc_tryconnect(RPC)
