#!/usr/bin/env python3
#Import cool new rpc module that gives us more control and gets rid of headaches :)
from pypresence import Presence
import time
import argparse
import sys
import os
#import info about system
from fetch_cord.args import parse_args
import fetch_cord.testing
from fetch_cord.out import cpuline, packagesline, termid, shellid, kernelline, gpuinfo, shell_line, termfontline, sysosline, sysosid
# define testing functions
uptime = testing.uptime
gpuid = testing.gpuid
desktopid = testing.desktopid
appid = testing.appid
cpuappid = testing.cpuappid
termappid = testing.termappid
args = parse_args()
#printing info with debug switch
if args.debug:
    print("run-rpc")
    print (uptime)
    print (packagesline[0])
    print (appid)
    print (gpuid)
print("Connecting")
print("RPC connection successful.")
time.sleep(5)
start_time = float(uptime) #discord uses unix time to interpret time for rich presnse, this is uptime in unix time    
if sysosid == "macos":
    devicetype = testing.devicetype
    product = testing.product
    bigicon = testing.bigicon
    ver = testing.ver
    client_id = '740822755376758944' #macos appid for discord rpc
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
        time.sleep(30)
def custom_time():
    ctime = int(args.time)
    time.sleep(ctime)

# cycle
def cycle0():
        global RPC
        if args.debug:
            print("cycle 0")
        client_id = appid
        RPC = Presence(client_id)
        RPC.connect()
        RPC.update(state=packagesline[0], 
        details=kernelline[0], 
        large_image="big",
        large_text=sysosline[0],
        small_image=desktopid,
        small_text=desktopid,
        start=start_time)
        
        if args.time:
            custom_time()
        else:
            time.sleep(30)
# cycle
def cycle1():
        global RPC
        if args.debug:
            print("cycle 1")
        client_id = cpuappid
        RPC = Presence(client_id)
        RPC.connect()
        RPC.update(state=cpuline[0], 
        details=gpuinfo, 
        large_image="big",
        large_text=cpuline[0],
        small_image=gpuid,
        small_text=gpuinfo,
        start=start_time)
        if args.time:
            custom_time()
        else:
            time.sleep(30)
# cycle
def cycle2():
        global RPC
        if args.debug:
            print("cycle 2")
        client_id = termappid
        RPC = Presence(client_id)
        RPC.connect()
        RPC.update(state=shell_line[0], 
        details=termfontline[0], 
        large_image="big",
        large_text=termid,
        small_image=shellid,
        small_text=shellid,
        start=start_time)
        if args.time:
            custom_time()
        else:
            time.sleep(30)
try:
    while True:
        if args.distro not in [args.shell, args.hardware]:
            cycle0()
        elif args.hardware not in [args.distro, args.shell]:
            cycle1()
        elif args.shell not in [args.distro, args.hardware]:
            cycle2()
        elif args.distro and args.hardware and not args.shell:
            cycle0()
            RPC.clear(pid=os.getpid())
            cycle1()
            RPC.clear(pid=os.getpid())
        elif args.distro and args.shell and not args.hardware:
            cycle0()
            RPC.clear(pid=os.getpid())
            cycle2()
            RPC.clear(pid=os.getpid())
        elif args.hardware and args.shell and not args.distro:
            cycle1()
            RPC.clear(pid=os.getpid())
            cycle2()
            RPC.clear(pid=os.getpid())
        else:
            cycle0()
            RPC.clear(pid=os.getpid())
            cycle1()
            RPC.clear(pid=os.getpid())
            cycle2()
            RPC.clear(pid=os.getpid())
except KeyboardInterrupt:
    print("Closing connection.")
    sys.exit(0)
