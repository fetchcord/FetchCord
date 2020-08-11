from fetch_cord.bash import exec_bash, BashError
import sys
import os
import argparse
from fetch_cord.args import parse_args
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
try:
    # only show the GPU in use with optimus, show both if prime render offload
    laptop = os.path.isdir("/sys/module/battery")
    if laptop:
        primeoffload = exec_bash("xrandr --listproviders | grep -o \"NVIDIA-0\"")
except BashError:
    primeoffload = ""
    pass
if nvidiagpuline:
    for n in range(len(nvidiagpuline)):
        gpuinfo += nvidiagpuline[n]
    gpuvendor += nvidiagpuline[0].split()[1]
if amdgpuline:
    try:
        if primeoffload == "":
            for a in range(len(amdgpurenderlist)):
                gpuinfo += amdgpurenderlist[a]
            gpuvendor += amdgpuvendor
    except NameError:
        pass

if intelgpuline:
    try:
        if primeoffload == "":
            gpuinfo += intelgpuline[0]
            gpuvendor += intelgpuline[0].split()[1]
    except NameError:
        pass

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
        print("deid %s" % deid)
        print("termfontline item 0: %s" % termfontline[0])
    except IndexError:
        pass
    print("sysosline: %s" % sysosline)
    print("amdgpurenderlist: %s" % amdgpurenderlist)
    print("amdgpurender: %s" % amdgpurender)
    print("gpuinfo %s" % gpuinfo)
    print("gpuvendor: %s" % gpuvendor)
    print("nvidiagpuline: %s" % nvidiagpuline)
    print("wmid: %s" % wmid)
    print("termid: %s" % termid)
    print("cpuvendor %s" % cpuvendor)
    print("cpumodel %s" % cpumodel)
    print("packagesline item 0: %s" % packagesline[0])
    print("cpuline item 0: %s" % cpuline[0])
    print("termline item 0: %s" % termline[0])
    print("sysosid: %s" % sysosid)
    print("sysosline item 0: %s" % sysosline[0])
    print("wmline item 0: %s"% wmline[0])
