#!/usr/bin/env python3
#import rpc file, made by https://github.com/niveshbirangal/discord-rpc, planning to make my own rpc soon
import rpc
import time
import argparse
#import info about system
from args import parse_args
import testing 
from out import cpuline, packagesline, termid, shellid, kernelline, gpuinfo, shell_line, termfontline, sysosline, sysosid
# define testing functions
uptime = testing.uptime
gpuid = testing.gpuid
desktopid = testing.desktopid
appid = testing.appid
cpuappid = testing.cpuappid
termappid = testing.termappid
args = parse_args()
#printing info(this will be removed soon)
print (uptime)
print (packagesline[0])
print (appid)
print (gpuid)
print("Connecting")
#client id of discord rpc app
print("RPC connection successful.")
time.sleep(5)
start_time = float(uptime) #discord uses unix time to interpret time for rich presnse, this is uptime in unix time
def set_id():
    # I hate discord
    global rpc_obj, rpc_obj2, rpc_obj3
    client_id = appid
    rpc_obj = rpc.DiscordIpcClient.for_platform(client_id)
    client_id2 = cpuappid
    rpc_obj2 = rpc.DiscordIpcClient.for_platform(client_id2)
    client_id3 = termappid
    rpc_obj3 = rpc.DiscordIpcClient.for_platform(client_id3)
def custom_time():
    ctime = int(args.time)
    time.sleep(ctime)
    

if sysosid == "macos":
    devicetype = testing.devicetype
    product = testing.product
    bigicon = testing.bigicon
    ver = testing.ver
    client_id = '740822755376758944' #macos appid for discord rpc
    print("RPC connection successful.")
    time.sleep(5)
    start_time = float(uptime[:-1])
    while True:
        activity = {
                "state": packagesline[0],
                "details": kernelline[0],
                "timestamps": {
                    "start": start_time
                },
                "assets": {
                    "small_text": product,
                    "small_image": devicetype,
                    "large_text": sysosline[0],
                    "large_image": bigicon
                }
            }
        rpc_obj.set_activity(activity)
        time.sleep(30)

# cycle
def cycle0():
        print("cycle 0")
        activity = {
            "state": packagesline[0],
            "details": kernelline[0],
            "timestamps": {
                "start": start_time
            },
            "assets": {
                "small_text": desktopid, #this will show de/wm name and de/wm version
                "small_image": desktopid, #this shows the de/wm logo
                "large_text": sysosline[0], #shows distro version and name on hover (refence to pretty name in /etc/os-release)
                "large_image": "big" #this will be the distro logo
            }
        }
        set_id()
        rpc_obj.set_activity(activity)
        if args.time:
            custom_time()
        else:
            time.sleep(30)
# cycle
def cycle1():
        print("cycle 1")
        activity = {
            "state": cpuline[0],
            "details": gpuinfo,
            "timestamps": {
                "start": start_time
            },
            "assets": {
                "small_text": gpuinfo, #this will show gpu(s)
                "small_image": gpuid, #this shows the GPU logo
                "large_text": cpuline[0], #shows CPU info and name on hover
                "large_image": "big" #this will be the CPU logo
            }
        }
        # reset id to make discord happy
        set_id()
        rpc_obj2.set_activity(activity)
        if args.time:
            custom_time()
        else:
            time.sleep(30)
# cycle
def cycle2():
        print("cycle 2")
        activity = {
            "state": shell_line[0],
            "details": termfontline[0],
            "timestamps": {
                "start": start_time
            },
            "assets": {
                "small_text": shellid, #this will show shell
                "small_image": shellid, #this shows the shell logo
                "large_text": termid, #shows terminal name on hover
                "large_image": "big" #this will be the terminal logo
            }
        }
        # reset id to make discord happy
        set_id()
        rpc_obj3.set_activity(activity)
        if args.time:
            custom_time()
        else:
            time.sleep(30)
while True:
    if args.distro:
        cycle0()
    elif args.hardware:
        cycle1()
    elif args.shell:
        cycle2()
    elif args.distro and args.hardware:
        cycle0()
        cycle1()
    elif args.distro and args.shell:
        cycle0()
        cycle2()
    elif args.hardware and args.shell:
        cycle1()
        cycle2()
    else:
        cycle0()
        cycle1()
        cycle2()
