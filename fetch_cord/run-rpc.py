#import rpc file, made by https://github.com/niveshbirangal/discord-rpc, planning to make my own rpc soon
from . import rpc
import time
#import info about system
from . import testing 
from .out import cpuline, packagesline, termid, shellid, kernelline, gpuinfo, cpuinfo, shell_line, termfontline, osline
# define testing functions
uptime = testing.uptime
gpuid = testing.gpuid
desktopid = testing.desktopid
appid = testing.appid
prettyname = testing.prettyname
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
    while True:
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
                "large_text": osline[0], #shows distro version and name on hover (refence to pretty name in /etc/os-release)
                "large_image": "big" #this will be the distro logo
            }
        }
        set_id()
        rpc_obj.set_activity(activity)
        time.sleep(30)
        cycle1()
# cycle
def cycle1():
    while True:
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
                "large_text": cpuinfo, #shows CPU info and name on hover
                "large_image": "big" #this will be the CPU logo
            }
        }
        # reset id to make discord happy
        set_id()
        rpc_obj2.set_activity(activity)
        time.sleep(30)
        cycle2()
# cycle
def cycle2():
    while True:
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
        time.sleep(30)
        cycle0()
cycle0()
