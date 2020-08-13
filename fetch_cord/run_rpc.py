# Import cool new rpc module that gives us more control and gets rid of headaches :)
from pypresence import Presence
import time
import sys
import os
# import info about system
from fetch_cord.args import parse_args
from fetch_cord.testing import uptime, gpuid, desktopid, appid, cpuappid, termappid
from fetch_cord.config import load_config, ConfigError
from fetch_cord.out import cpuline, packagesline, termid, shellid, kernelline, gpuinfo, shell_line, termfontline, \
    sysosline, sysosid, kernel, packages, gpu, cpu, shell, termfont

args = parse_args()


def main():
    # printing info with debug switch
    if args.debug:
        print("run-rpc")
        print(uptime)
        print(packagesline[0])
        print(appid)
        print(gpuid)
    if sysosid.lower() == "macos":
        runmac()
    else:
        config = get_config()
        loonix(config)


print("Connecting")
print("RPC connection successful.")
time.sleep(5)
# discord uses unix time to interpret time for rich presnse, this is uptime in unix time
start_time = float(uptime)


def get_config():

    try:
        config = load_config()
        print(config)
    except ConfigError as e:
        print("Error loading config file, using default values." % str(e))
    return config

def runmac():
    from fetch_cord.testing import devicetype, product, bigicon, ver
    client_id = '740822755376758944'  # macos appid for discord rpc
    time.sleep(5)
    start_time = float(uptime[:-1])
    while True:
        RPC = Presence(client_id)
        RPC.connect()
        RPC.update(state=packagesline[0], #uptadte state as packages
        details=kernelline[0], # update details as kernel
        large_image=bigicon, #set icon
        large_text=sysosline[0], #set large icon text
        small_image=devicetype, #set small image icon
        small_text=product, #set small image text
        start=start_time)
        if args.time:
            custom_time()
        else:
            time.sleep(30)


def custom_time():
    ctime = int(args.time)
    time.sleep(ctime)


# cycle


def cycle0(config):
    global RPC
    top_line = config["cycle_0"]["top_line"]
    if top_line == "kernel":
        top_line = kernel
    else:
        top_line = pacakges
    bottom_line = config["cycle_0"]["bottom_line"]
    if bottom_line == "kernel":
        bottom_line = kernel
    else:
        bottom_line = packages
    if args.debug:
        print("cycle 0")
    client_id = appid
    RPC = Presence(client_id)
    RPC.connect()
    RPC.update(state=bottom_line, 
    details=top_line, 
    large_image="big",
    large_text=sysosline[0],
    small_image=desktopid,
    small_text=desktopid,
    start=start_time)
    if args.debug:
        print("appid: %s" % client_id)
     
    config_time = config["cycle_0"]["time"]

    if args.time:
        custom_time()
    elif config_time:
        time.sleep(int(config_time))
    elif args.distro and not args.shell and not args.hardware:
        time.sleep(9999)
    else:
        time.sleep(30)


# cycle


def cycle1(config):
    global RPC
    top_line = config["cycle_1"]["top_line"]
    if top_line == "gpu":
        top_line = gpu
    else:
        top_line = cpu
    bottom_line = config["cycle_1"]["bottom_line"]
    if bottom_line == "gpu":
        bottom_line = gpu
    else:
        bottom_line = cpu
    if args.debug:
        print("cycle 1")
    client_id = cpuappid
    RPC = Presence(client_id)
    RPC.connect()
    RPC.update(state=bottom_line, 
    details=top_line, 
    large_image="big",
    large_text=cpuline[0],
    small_image=gpuid,
    small_text=gpuinfo,
    start=start_time)
    if args.debug:
        print("appid: %s" % client_id)

    config_time = config["cycle_1"]["time"]

    if args.time:
        custom_time()
    elif config_time:
        time.sleep(int(config_time))
    elif args.hardware and not args.distro and not args.shell:
        time.sleep(9999)
    else:
        time.sleep(30)


# cycle


def cycle2(config):
    global RPC
    top_line = config["cycle_2"]["top_line"]
    if top_line == "termfont":
        top_line = termfont
    else:
        top_line = shell
    bottom_line = config["cycle_2"]["bottom_line"]
    if bottom_line == "termfont":
        bottom_line = termfont
    else: 
        bottom_line = shell
    if args.debug:
        print("cycle 2")
    client_id = termappid
    RPC = Presence(client_id)
    RPC.connect()
    RPC.update(state=bottom_line, 
    details=top_line, 
    large_image="big",
    large_text=termid,
    small_image=shellid,
    small_text=shellid,
    start=start_time)
    if args.debug:
        print("appid: %s" % client_id)

    config_time = config["cycle_2"]["time"]

    if args.time:
        custom_time()
    elif config_time:
        time.sleep(int(config_time))
    elif args.shell and not args.distro and not args.hardware:
        time.sleep(9999)
    else:
        time.sleep(30)

def loonix(config):
    try:
        while True:
            if args.distro not in [args.shell, args.hardware]:
                cycle0(config)
            elif args.hardware not in [args.distro, args.shell]:
                cycle1(config)
            elif args.shell not in [args.distro, args.hardware]:
                cycle2(config)
            elif args.distro and args.hardware and not args.shell:
                cycle0(config)
                RPC.clear(pid=os.getpid())
                cycle1(config)
                RPC.clear(pid=os.getpid())
            elif args.distro and args.shell and not args.hardware:
                cycle0(config)
                RPC.clear(pid=os.getpid())
                cycle2(config)
                RPC.clear(pid=os.getpid())
            elif args.hardware and args.shell and not args.distro:
                cycle1(config)
                RPC.clear(pid=os.getpid())
                cycle2(config)
                RPC.clear(pid=os.getpid())
            else:
                cycle0(config)
                RPC.clear(pid=os.getpid())
                cycle1(config)
                RPC.clear(pid=os.getpid())
                cycle2(config)
                RPC.clear(pid=os.getpid())
    except KeyboardInterrupt:
        print("Closing connection.")
        sys.exit(0)
