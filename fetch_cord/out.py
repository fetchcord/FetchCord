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
neofetchwin = ""
if os.name == "nt":
    neofetchwin = os.popen("neofetch --noart").read()
else:
    home = exec_bash("echo $HOME")
    if os.path.isdir("%s/.var/app/com.discordapp.Discord" % home) and not os.path.isfile("/usr/bin/discord") and not os.path.isdir("/opt/Discord"):
        try:
            print("Symlinking XDG_RUNTIME_DIR path for Flatpak Discord.")
            exec_bash(
                "cd %s/.var && ln -sf {app/com.discordapp.Discord,$XDG_RUNTIME_DIR}/discord-ipc-0 " % home)
        except BashError as e:
            print("Could not symlink XDG_RUNTIME_DIR Error: %s" % str(e))

# use default neofetch output, ignoring user config
baseinfo = exec_bash("neofetch --stdout --config none")

# make lists
cpu = "CPU:"
cpuline = []
nvidiagpu = "GPU: NVIDIA"
nvidiagpuline = []
amdgpu = "GPU: AMD"
amdgpuline = []
intelgpu = "GPU: Intel"
intelgpuline = []
vmwaregpu = "GPU: VMware"
vmwaregpuline = []
virtiogpu = "GPU: 00:02.0 Red"
virtiogpuline = []
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
mem = "Memory:"
memline = []
mobo = "Motherboard:"
moboline = []
packages = "Packages:"
packagesline = []
host = "Host:"
hostline= []
res = "Resolution:"
resline = []
if neofetchwin != "":
    filepath = "%userprofile%\\AppData\\Local\\Temp"
    with open(filepath, 'w') as f:
        print(neofetchwin, file=f)
    with open(filepath, 'rt') as f:
        for line in f:
            if line.find(cpu) != -1:
                cpuline.append(line.rstrip('\n'))
            if line.find(nvidiagpu) != -1:
                nvidiagpuline.append(line.rstrip('\n'))
            if line.find(amdgpu) != -1:
                amdgpuline.append(line.rstrip('\n'))
            if line.find(intelgpu) != -1:
                intelgpuline.append(line.rstrip('\n'))
            if line.find(vmwaregpu) != -1:
                vmwaregpuline.append(line.rstrip('\n'))
            if line.find(sysos) != -1:
                sysosline.append(line.rstrip('\n'))
            if line.find(mem) != -1:
                memline.append(line.rstrip('\n'))
            if line.find(mobo) != -1:
                moboline.append(line.rstrip('\n'))

elif neofetchwin == "":
    filepath = "/tmp/out.txt"
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
            if line.find(vmwaregpu) != -1:
                vmwaregpuline.append(line.rstrip('\n'))
            if line.find(virtiogpu) != -1:
                virtiogpuline.append(line.rstrip('\n'))
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
            if line.find(host) != -1:
                hostline.append(line.rstrip('\n'))
            if line.find(res) != -1:
                resline.append(line.rstrip('\n'))
try:
    if os.path.isfile(filepath):
        os.remove(filepath)
except FileNotFoundError:
    pass
sysosid = sysosline[0].split()[1]
gpuvendor = ""
gpuinfo = ""
primeoffload = ""
if sysosid.lower() not in ["windows", "macos"]:
    try:
        # only show the GPU in use with optimus, show both if prime render offload
        laptop = os.path.isdir("/sys/module/battery")
        if laptop and nvidiagpuline:
            if args.debug:
                print("laptop: %s" % laptop)
            primeoffload = exec_bash("xrandr --listproviders | grep -o \"NVIDIA-0\"")
    except BashError:
        pass

if nvidiagpuline:

    for n in range(len(nvidiagpuline)):
        gpuinfo += nvidiagpuline[n]
    gpuvendor += nvidiagpuline[0].split()[1]

amdgpurenderlist = []
if amdgpuline and sysosid.lower() not in ['windows', 'macos'] and primeoffload == "":

    try:
        # amd GPUs
        for i in range(len(amdgpuline)):
            env_prime = "env DRI_PRIME=%s" % i
            amdgpurender = "GPU: " + \
                exec_bash(
                    "%s glxinfo | grep \"OpenGL renderer string:\" | sed 's/^.*: //;s/(.*//'" % env_prime) + ' '
            amdgpurenderlist = []
            if i != -1:
                amdgpurenderlist.append(amdgpurender)
        amdgpuvendor = amdgpurender.split()[1]
    except BashError as e:
        print("ERROR: Could not run glxinfo [%s]" % str(e))
        sys.exit(1)

    for a in range(len(amdgpurenderlist)):
        gpuinfo += amdgpurenderlist[a]
    gpuvendor += amdgpuvendor

elif amdgpurenderlist == [] and primeoffload == "":
    try:
        for a in range(len(amdgpuline)):
            gpuinfo += amdgpuline[a]
        gpuvendor += amdgpuline[0].split()[1]
    except IndexError:
        pass

if intelgpuline and primeoffload == "":

    try:
        gpuinfo += intelgpuline[0]
        gpuvendor += intelgpuline[0].split()[1]
    except IndexError:
        pass

if vmwaregpuline:
    gpuinfo = vmwaregpuline[0]
    gpuvendor = vmwaregpuline[0].split()[1]
if virtiogpuline:
    gpuinfo = vitriogpuline[0]
    gpuvendor = virtiogpuline[0].split()[2:3].join()

cpusplit = cpuline[0].split()[:-1]
s=' '.join(cpusplit)
cpuinfo = s + ' ' + cpuline[0].split()[-1].replace("0", "")
cpuvendor = cpuline[0].split()[1]
cpumodel = ""
if cpuvendor == "Intel":
    cpumodel = cpuline[0].replace(
        '-', ' ').split()[1] + ' ' + cpuline[0].replace('-', ' ').split()[2]
elif cpuvendor == "AMD":
    cpumodel = cpuline[0].split()[2] + ' ' + cpuline[0].split()[3]
# fuck you intel
elif cpuvendor == "Pentium":
    cpumodel = cpuline[0].split()[1]
if wmline:
    wmid = wmline[0].split()[1]
else:
    wmid = "N/A"

termid = termline[0].split()[1]
if args.terminal:
    terminals = ['kitty', 'st', 'gnome-terminal',
                 'konsole', 'alacritty', 'xterm', 'cool-retro-term']
    if args.terminal in terminals:
        termid = args.terminal
    else:
        print("Invalid terminal, only %s are supported.\n"
              "Please make a github issue if you would like to have your terminal added.\n"
              "https://github.com/MrPotatoBobx/FetchCord" % terminals)
        sys.exit(1)

shellid = shell_line[0].split()[1]
kernelid = kernelline[0].split()[1]
sysosid = sysosline[0].split()[1]
if sysosid.lower() in ['windows', 'linux', 'opensuse']:
    sysosid = sysosline[0].split()[1] + sysosline[0].split()[2]
if termfontline and args.termfont:
    print("Custom terminal font not set because a terminal font already exists, %s" %
          termfontline[0])
elif not termfontline:
    termfontline = []
    if args.termfont:
        termfontline.append("Terminal Font: " + args.termfont)
    else:
        termfontline.append("Terminal font: N/A")
if deline:
    deid = deline[0].split()[1]
else:
    deid = "N/A"
dewmid = ""
if deline and wmline:
    dewmid = deline[0] + ' ' + wmline[0]
elif deline and not wmline:
    dewmid = deline[0]
elif wmline and not deline:
    dewmid = wmline[0]
hostid = ""
if hostline:
    hostid = hostline[0].split()[1]
if laptop:
    lapordesk = "laptop"
else:
    lapordesk = "desktop"
if not resline:
    resline = "Resolution: N/A"
else:
    resline = resline[0]
if args.debug:
    print("out")
    try:
        print("deid %s" % deid)
        print("termfontline item 0: %s" % termfontline[0])
    except NameError:
        pass
    print("sysosline: %s" % sysosline)
    try:
        print("amdgpurenderlist: %s" % amdgpurenderlist)
        print("amdgpurender: %s" % amdgpurender)
    except NameError:
        pass
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
    try:
        print("wmline item 0: %s" % wmline[0])
        print("hostid: %s" % hostid)
    except IndexError:
        pass
