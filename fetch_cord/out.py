from bash import exec_bash, BashError
import subprocess
import os
import argparse
import sys
from args import parse_args
args = parse_args()
if args.time:
    if int(args.time) < 15:
        print("ERROR: Invalid time set, must be > 15 seconds, cannot continue.")
        sys.exit(1)
    else:
        print("setting custom time %s" % args.time)
try:
    if args.help:
        sys.exit(0)
except AttributeError:
    pass
home = exec_bash("echo $HOME")
if os.path.isdir("%s/.var/app/com.discordapp.Discord" % home) and not os.path.isdir("/usr/bin/discord" or not os.path.isdir("/opt/Discord")):
    try:
        exec_bash("cd %s/.var && ln -sf {app/com.discordapp.Discord,$XDG_RUNTIME_DIR}/discord-ipc-0 "% home)
    except BashError as e:
        print("Could not symlink XDG_RUNTIME_DIR Error: %s" % str(e))
# use default neofetch output, ignoring user config
baseinfo = exec_bash("neofetch --stdout --config none")
#make lists
cpu = "CPU:"
cpuline = []
nvidiagpu = "GPU: NVIDIA"
nvidiagpuline = []
amdgpu = "GPU: AMD"
amdgpuline = []
intelgpu = "GPU: Intel"
intelgpuline = []
term = "Terminal:"
termline = []
termfont = "Terminal Font:"
termfontline = []
wm = "WM:"
wmline = []
de = "DE:"
deline = []
shell = "Shell:"
shell_line = []
kernel = "Kernel:"
kernelline = []
sysos = "OS:"
sysosline = []
packages = "Packages:"
packagesline = []
filepath="/tmp/out.txt"
with open(filepath, 'w') as f:
    print(baseinfo, file=f)
with open(filepath, "rt") as f:
    for line in f:
        if line.find(cpu) != -1:
            cpuline.append(line.rstrip('\n'))
        if line.find(nvidiagpu) != -1:
            nvidiagpuline.append(line.rstrip('\n'))
        if line.find(amdgpu) != -1:
            amdgpuline.append(line.rstrip('\n'))
        if line.find(intelgpu) != -1:
            intelgpuline.append(line.rstrip('\n'))
        if line.find(term) != -1:
            termline.append(line.rstrip('\n'))
        if line.find(termfont) != -1:
            termfontline.append(line.rstrip('\n'))
        if line.find(de) != -1:
            deline.append(line.rstrip('\n'))
        if line.find(wm) != -1:
            wmline.append(line.rstrip('\n'))
        if line.find(shell) != -1:
            shell_line.append(line.rstrip('\n'))
        if line.find(packages) != -1:
            packagesline.append(line.rstrip('\n'))
        if line.find(kernel) != -1:
            kernelline.append(line.rstrip('\n'))
        if line.find(sysos) != -1:
            sysosline.append(line.rstrip('\n'))
try:
    if os.path.isfile(filepath):
        os.remove(filepath)
except FileNotFoundError:
    pass
gpuvendor = "none"
sysosid = sysosline[0].split()[1]
if amdgpuline and sysosid.lower() != "macos" and sysosid.lower() != "windows":
    try:
        # amd GPUs
        for i in range(len(amdgpuline)):
            env_prime = "env DRI_PRIME=%s" % i
            amdgpurender = "GPU: " + exec_bash("%s glxinfo | grep \"OpenGL renderer string:\" | sed 's/^.*: //;s/(.*//'" % env_prime)
            amdgpurenderlist = []
            if i != -1:
                amdgpurenderlist.append(amdgpurender)
            gpuvendor = amdgpurender.split()[1]
            amdgpuvendor = amdgpurender.split()[1]
            gpuid = amdgpurender
    except BashError as e:
        print("ERROR: Could not run glxinfo [%s]" % str(e))
        sys.exit(1)
gpuvendor = ""
gpuinfo = ""
if nvidiagpuline:
    for n in range(len(nvidiagpuline)):
        gpuinfo += nvidiagpuline[n]
    gpuvendor += nvidiagpuline[0].split()[1]
if amdgpuline:
    for a in range(len(amdgpurenderlist)):
        gpuinfo += amdgpurenderlist[a]
    gpuvendor += amdgpuvendor
if intelgpuline:
    gpuinfo += intelgpuline[0]
    gpuvendor += intelgpuline[0].split()[1]

cpuvendor = cpuline[0].split()[1] 
if cpuvendor == "Intel":
    cpumodel = cpuline[0].replace('-', ' ').split()[1] + ' ' + cpuline[0].replace('-', ' ').split()[2]
elif cpuvendor == "AMD":
    cpumodel = cpuline[0].split()[2] + ' ' + cpuline[0].split()[3]
wmid = wmline[0].split()[1]
termid = termline[0].split()[1]
shellid = shell_line[0].split()[1]
kernelid = kernelline[0].split()[1]
sysosid = sysosline[0].split()[1]
if sysosid.lower() in ['windows', 'linux', 'opensuse']:
    sysosid = sysosline[0].split()[1] + sysosline[0].split()[2]
if not termfontline:
    termfontline = []
    termfontline.append("Terminal font: N/A")
if deline:
    deid = deline[0].split()[1]
else:
    deid = "none"
if args.debug:
    print("out")
    try:
        print(deid)
        print(termfontline[0])
    except IndexError:
        pass
    print(sysosline)
    print(amdgpurenderlist)
    print(amdgpurender)
    print(gpuinfo)
    print(gpuvendor)
    print(nvidiagpuline)
    print(wmid)
    print(termid)
    print(cpuvendor)
    print(cpumodel)
    print(packagesline[0])
    print(cpuline[0])
    print(termline[0])
    print(sysosid)
    print(sysosline[0])
    print(wmline[0])
