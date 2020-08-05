#import rpc file, made by https://github.com/niveshbirangal/discord-rpc, planning to make my own rpc soon
import rpc
import time
#import info about system
from testing import appid, cpuid, text, packtext, uptime, prettyname, desktopid
#printing info(this will be removed soon)
print (uptime)
print (text)
print (packtext)
print (appid)
print("Connecting")
#client id of discord rpc app
client_id = appid 
rpc_obj = rpc.DiscordIpcClient.for_platform(client_id) #Send the client ID to the rpc module
print (desktopid)
print (cpuid)
print("RPC connection successful.")
time.sleep(5)
start_time = float(uptime) #discord uses unix time to interpret time for rich presnse, this is uptime in unix time
# main loop
    # sub loops
def cycle0():
    while True:
        print("cycle 0")
        activity = {
#            "test": cpu,
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
        print("cycle 0")
        activity = {
#            "test": cpu,
            "state": packtext,
            "details": cpuid,
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
        cycle0()
cycle1()
