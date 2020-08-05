#import rpc file, made by https://github.com/niveshbirangal/discord-rpc, planning to make my own rpc soon
import rpc
import time
#import info about system
from testing import appid, text, packtext, uptime, prettyname, desktopid
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
print("RPC connection successful.")
time.sleep(5)
start_time = float(uptime) #discord uses unix time to interpret time for rich presnse, this is uptime in unix time
while True:
    activity = {
            "state": packtext,
            "details": text,
            "timestamps": {
                "start": start_time
            },
            "assets": {
                "small_text": "KDE Plasma", #static atm, will show de/wm name and version
                "small_image": desktopid, #static atm, will show de/wm logo
                "large_text": prettyname, #shows distro version and name on hover (refence to pretty name in /etc/os-release)
                "large_image": "big" #this will be the discord logo
            }
        }
    rpc_obj.set_activity(activity)
    time.sleep(30)
