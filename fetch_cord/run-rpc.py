#import rpc file, made by https://github.com/niveshbirangal/discord-rpc, planning to make my own rpc soon
from . import rpc
import time
import argparse
#import info about system
from .args import parse_args
from . import testing 
from .out import cpuline, packagesline, termid, shellid, kernelline, gpuinfo, shell_line, termfontline, sysosline
# define testing functions
uptime = testing.uptime
gpuid = testing.gpuid
desktopid = testing.desktopid
appid = testing.appid
cpuappid = testing.cpuappid
termappid = testing.termappid
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
        if not args.distro:
            set_id()
        rpc_obj.set_activity(activity)
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
        if not args.hardware:
            set_id()
        rpc_obj2.set_activity(activity)
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
        if not args.shell:
            set_id()
        rpc_obj3.set_activity(activity)
        time.sleep(30)
args = parse_args()
if args.distro:
    client_id = appid
    rpc_obj = rpc.DiscordIpcClient.for_platform(client_id)
    while True:
        cycle0()
if args.hardware:
    client_id2 = cpuappid
    rpc_obj2 = rpc.DiscordIpcClient.for_platform(client_id2)
    while True:
        cycle1()
if args.shell:
    client_id3 = termappid
    rpc_obj3 = rpc.DiscordIpcClient.for_platform(client_id3)
    while True:
        cycle2()
if not args.distro:
    while True:
        cycle0()
        cycle1()
        cycle2()
