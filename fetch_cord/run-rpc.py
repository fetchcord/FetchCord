#import rpc file, made by https://github.com/niveshbirangal/discord-rpc, planning to make my own rpc soon
from . import rpc
import time
#import info about system
from . import testing 
# define testing functions
uptime = testing.uptime
text = testing.text
packtext = testing.packtext
appid = testing.appid
gpuid = testing.gpuid
cpumodel = testing.cpumodel
desktopid = testing.desktopid
prettyname = testing.prettyname
gpu = testing.gpu
cpuinfo = testing.cpuinfo
cpuappid = testing.cpuappid
gpuout = testing.gpuout
gpuinfo = testing.gpuinfo
#printing info(this will be removed soon)
print (uptime)
print (text)
print (packtext)
print (appid)
print (gpuid)
print (cpumodel)
print("Connecting")
#client id of discord rpc app
print("RPC connection successful.")
#client_id = appid
#rpc_obj = rpc.DiscordIpcClient.for_platform(client_id)
time.sleep(5)
start_time = float(uptime) #discord uses unix time to interpret time for rich presnse, this is uptime in unix time
def set_id():
    global rpc_obj, rpc_obj2 
    client_id = appid
    rpc_obj = rpc.DiscordIpcClient.for_platform(client_id)
    client_id2 = cpuappid
    rpc_obj2 = rpc.DiscordIpcClient.for_platform(client_id2)
# cycle
def cycle0():
    while True:
        print("cycle 0")
        activity = {
            "state": packtext,
            "details": text,
            "timestamps": {
                "start": start_time
            },
            "assets": {
                "small_text": desktopid, #this will show de/wm name and de/wm version
                "small_image": desktopid, #this shows the de/wm logo
                "large_text": prettyname, #shows distro version and name on hover (refence to pretty name in /etc/os-release)
                "large_image": "big" #this will be the distro logo
            }
        }
        rpc_obj.set_activity(activity)
        time.sleep(30)
        break
# cycle
def cycle1():
    while True:
        print("cycle 1")
        activity = {
            "state": cpumodel,
            "details": gpuout,
            "timestamps": {
                "start": start_time
            },
            "assets": {
                "small_text": gpuinfo, #this will show de/wm name and de/wm version
                "small_image": gpuid, #this shows the de/wm logo
                "large_text": cpuinfo, #shows distro version and name on hover (refence to pretty name in /etc/os-release)
                "large_image": "big" #this will be the distro logo
            }
        }
        # reset id to make discord happy
        set_id()
        rpc_obj2.set_activity(activity)
        time.sleep(30)
        cycle0()
cycle1()
