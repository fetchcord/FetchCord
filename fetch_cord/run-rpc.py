#import rpc file, made by https://github.com/niveshbirangal/discord-rpc, planning to make my own rpc soon
from . import rpc
import time
#import info about system
from .testing import appid, appid2, cpuid, text, packtext, uptime, prettyname, desktopid, cpumodel, gpu, cpuappid
#printing info(this will be removed soon)
print (uptime)
print (text)
print (packtext)
print (appid)
print (cpumodel)
print("Connecting")
#client id of discord rpc app
print("RPC connection successful.")
#client_id = appid
#rpc_obj = rpc.DiscordIpcClient.for_platform(client_id)
time.sleep(5)
start_time = float(uptime) #discord uses unix time to interpret time for rich presnse, this is uptime in unix time
client_id = appid
rpc_obj = rpc.DiscordIpcClient.for_platform(client_id)
client_id2 = appid2
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
        activity1 = {
            "state": cpumodel,
            "details": gpu,
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
        rpc_obj2.set_activity(activity1)
        time.sleep(30)
        cycle0()
cycle1()
