from . import rpc
import time
import os
from .mactesting import uptime, product, appsp, kernel, ver, devicetype, bigicon
print("Conecting")
client_id = '740822755376758944' #macos appid for discord rpc
rpc_obj = rpc.DiscordIpcClient.for_platform(client_id) #Send the client ID to the rpc module
print("RPC connection successful.")
time.sleep(5)
start_time = float(uptime[:-1])
while True:
    activity = {
            "state": appsp,
            "details": "Kernel: " + kernel,
            "timestamps": {
                "start": start_time
            },
            "assets": {
                "small_text": product,
                "small_image": devicetype,
                "large_text": "MacOS" + ' ' + ver,
                "large_image": bigicon
            }
        }
    rpc_obj.set_activity(activity)
    time.sleep(30)
