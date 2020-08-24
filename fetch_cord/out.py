from fetch_cord.bash import exec_bash, BashError
import sys
import os
from fetch_cord.args import parse_args
from fetch_cord.update import update


args = parse_args()


if args.update:
    update()


if args.time:
    if int(args.time) < 15:
        print("ERROR: Invalid time set, must be > 15 seconds, cannot continue.")
        sys.exit(1)
    else:
        print("setting custom time %s seconds" % args.time)

try:
    if args.help:
        sys.exit(0)
except AttributeError:
    pass

neofetchwin = False
if os.name == "nt":
    neofetchwin = os.popen("neofetch --noart").read()
else:
    home = os.getenv('HOME')
    if os.path.isdir("%s/.var/app/com.discordapp.Discord" % home) and not os.path.isfile("/usr/bin/discord") and not os.path.isdir("/opt/Discord"):
        try:
            print("Symlinking XDG_RUNTIME_DIR path for Flatpak Discord.")
            exec_bash(
                "cd %s/.var && ln -sf {app/com.discordapp.Discord,$XDG_RUNTIME_DIR}/discord-ipc-0 " % home)
        except BashError as e:
            print("Could not symlink XDG_RUNTIME_DIR Error: %s" % str(e))

    # use default neofetch output, ignoring user config
    baseinfo = exec_bash("neofetch --stdout --config none --cpu_temp C")
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
theme = "Theme:"
themeline = []
if neofetchwin:
    nvidiagpu = "NVIDIA"
    radgpu = "Radeon"
    intelgpu = "Intel"
    radgpuline = []
    filepath = "tmp.txt"
    with open(filepath, 'w') as f:
        print(neofetchwin, file=f)
    with open(filepath, 'rt') as f:
        for line in f:
            if line.find(cpu) != -1:
                cpuline.append(line.rstrip('\n'))
            if line.find(nvidiagpu) != -1:
                nvidiagpuline.append(line[line.find(nvidiagpu):].rstrip('\n'))
            if line.find(amdgpu) != -1:
                amdgpuline.append(line.rstrip('\n'))
            if line.find(intelgpu) != -1 and line.find(cpu) == -1:
                intelgpuline.append(line[line.find(intelgpu):].rstrip('\n'))
            if line.find(vmwaregpu) != -1:
                vmwaregpuline.append(line.rstrip('\n'))
            if line.find(sysos) != -1:
                sysosline.append(line.rstrip('\n'))
            if line.find(mem) != -1:
                memline.append(line.rstrip('\n'))
            if line.find(mobo) != -1:
                moboline.append(line.rstrip('\n'))
            if line.find(radgpu) != -1:
                radgpuline.append(line[line.find(radgpu):].rstrip('\n'))

elif not neofetchwin:
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
            if line.find(mem) != -1:
                memline.append(line.rstrip('\n'))
            if line.find(theme) != -1:
                themeline.append(line.rstrip('\n'))
try:
    if os.path.isfile(filepath):
        os.remove(filepath)
except FileNotFoundError:
    pass
sysosid = sysosline[0].split()[1]
gpuvendor = ""
gpuinfo = ""
primeoffload = False
if sysosid.lower() != "macos" and os.name != "nt":
        # only show the GPU in use with optimus, show both if prime render offload
        batpath = "/sys/class/power_supply"
        laptop = False
        for i in os.listdir(batpath):
            if i.startswith("BAT"):
                laptop = True
        if laptop and nvidiagpuline:
            if args.debug:
                print("laptop: %s" % laptop)
            try:
                primeoffload = exec_bash("xrandr --listproviders | grep -o \"NVIDIA-0\"")
            except BashError:
                pass

amdgpurenderlist = []
if os.name != "nt":
    if nvidiagpuline:
        for n in range(len(nvidiagpuline)):
            gpuinfo += nvidiagpuline[n]
        gpuvendor += "NVIDIA"

    if amdgpuline and sysosid.lower() not in ['windows', 'macos'] and not primeoffload:
        try:
            # amd GPUs
            for i in range(len(amdgpuline)):
                # assume DRI_PRIME=0 is the intel GPU
                if laptop and intelgpuline:
                    i = i + 1
                env_prime = "env DRI_PRIME=%s" % i
                amdgpurender = "GPU: " + \
                    exec_bash(
                        "%s glxinfo | grep \"OpenGL renderer string:\" | sed 's/^.*: //;s/[(][^)]*[)]//g'" % env_prime) + ' '
                if i != -1:
                    amdgpurenderlist.append(amdgpurender)
            amdgpuvendor = "AMD"
        except BashError as e:
            print("ERROR: Could not run glxinfo [%s]" % str(e))
            sys.exit(1)

        for a in range(len(amdgpurenderlist)):
            gpuinfo += amdgpurenderlist[a]
        gpuvendor += "AMD"

    elif amdgpurenderlist == [] and not primeoffload:
        try:
            for a in range(len(amdgpuline)):
                gpuinfo += amdgpuline[a]
            gpuvendor += amdgpuline[0].split()[1]
        except IndexError:
            pass

    if intelgpuline and not primeoffload:
        try:
            gpuinfo += intelgpuline[0]
            gpuvendor += intelgpuline[0].split()[1]
        except IndexError:
            pass
else: # Cursed windows stuff
    if nvidiagpuline:
        try:
            gpuinfo += "GPU: " +  nvidiagpuline[0]
            for n in nvidiagpuline[1:]:
                gpuinfo += "\nGPU: " + n

            gpuvendor += nvidiagpuline[0].split()[0]
        except IndexError:
            pass
    if radgpuline:
        try:
            if nvidiagpuline:
                gpuinfo += "\n"
            gpuinfo += "GPU: " + radgpuline[0]
            for r in radgpuline[1:]:
                gpuinfo += "\nGPU: " + r

            gpuvendor += "AMD"
        except IndexError:
            pass
    if intelgpuline:
        try:
            if nvidiagpuline or radgpuline:
                gpuinfo += "\n"
            gpuinfo += "GPU: " + intelgpuline[0]
            for i in intelgpuline[1:]:
                gpuinfo += "\nGPU: " + i

            gpuvendor += "Intel"
        except IndexError:
            pass

if vmwaregpuline:
    gpuinfo = vmwaregpuline[0]
    gpuvendor = vmwaregpuline[0].split()[1]
if virtiogpuline:
    gpuinfo = virtiogpuline[0]
    gpuvendor = virtiogpuline[0].split()[2:3].join()

if os.name != "nt":
    cpusplit = cpuline[0].split()[:-2]
    s=' '.join(cpusplit)
    cpuinfo = s + ' ' + cpuline[0].split()[-2].replace("0G", "G", 1) + ' ' + cpuline[0].split()[-1]
else:
    cpusplit = cpuline[0].split()[:-1]
    s=' '.join(cpusplit)
    # I fucking hate you intel
    cpuinfo = s + ' ' + cpuline[0].split()[-1].replace("0", "", 1).replace("Core(TM)2", "Core 2").replace("Intel(R)", "Intel").replace("Core(TM)", "Core")
cpuvendor = cpuline[0].split()[1].replace("Intel(R)", "Intel")
cpumodel = ""
if cpuvendor == "Intel":
    if os.name != "nt":
        cpumodel = cpuline[0].replace(
            '-', ' ').split()[1] + ' ' + cpuline[0].replace('-', ' ').split()[2]
        if cpumodel == "Intel Core":
            cpumodel = cpuline[0].split()[1:5]
            cpumodel = ' '.join(cpumodel)
    else:
        cpumodel = cpuline[0].replace(
            '-', ' ').split()[1].replace("Intel(R)", "Intel") + ' ' + cpuline[0].replace('-', ' ').split()[3]
        if cpumodel == "Intel 2" or cpumodel == "Intel Solo":
            cpumodel = cpuline[0].split()[1:5]
            cpumodel = ' '.join(cpumodel)

elif cpuvendor == "AMD":
    cpumodel = cpuline[0].split()[2] + ' ' + cpuline[0].split()[3]
# fuck you intel
elif cpuvendor == "Pentium":
    cpumodel = cpuline[0].split()[1]

if os.name != "nt":
    # linux shit
    if wmline:
        wmid = wmline[0].split()[1]
    else:
        wmid = "N/A"
    termid = ""
    try:
        if termline:
            termid = termline[0].split()[1]
        else:
            termid = "N/A"
            termline = ["N/A"]
    except IndexError:
        pass
    shellid = shell_line[0].split()[1]
    if termfontline:
        termfontsplit = termfontline[0].split()[1:]
        s=' '.join(termfontsplit)
        termfontline = s
    if termfontline and args.termfont:
        print("Custom terminal font not set because a terminal font already exists, %s" %
            termfontline)
    elif not termfontline:
        if args.termfont:
            termfontline = "Font: " + args.termfont
        else:
            termfontline = "Font: N/A"
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
    lapordesk = ""
    if not hostline:
        hostline = ""
    try:
        if laptop and sysosid.lower() != 'macos':
            lapordesk = "laptop"
        else:
            lapordesk = "desktop"
    except NameError:
        pass
    if not resline:
        resline = "Resolution: N/A"
    else:
        resline = resline[0]
    kernelid = kernelline[0].split()[1]
    if not themeline:
        themeline = ["N/A"]
    if not memline:
        memline = ["N/A"]
if sysosid.lower() in ['windows', 'linux', 'opensuse']:
    sysosid = sysosline[0].split()[1] + sysosline[0].split()[2]


if args.debug:
    print("----out.py----\n")
    print("----DE/WM----")
    if os.name != "nt":
        print("deid: %s" % deid)
        print("wmid: %s" % wmid)
        try:
            print("wmline item 0: %s" % wmline[0])
        except IndexError:
            pass
        print("\n----TERMINAL----\n")
        print("termfontline: %s" % termfontline)
        print("termid: %s" % termid)
        print("termline item 0: %s" % termline[0])
        print("themeline: %s" % themeline)
    print("\n----GPU INFO----\n")
    try:
        print("amdgpurenderlist: %s" % amdgpurenderlist)
        print("amdgpurender: %s" % amdgpurender)
    except NameError:
        pass
    print("nvidiagpuline: %s" % nvidiagpuline)
    print("intelgpuline: %s" % intelgpuline)
    print("gpuinfo: %s" % gpuinfo)
    print("gpuvendor: %s" % gpuvendor)
    print("\n----CPU INFO----\n")
    print("cpuvendor: %s" % cpuvendor)
    print("cpumodel: %s" % cpumodel)
    print("cpuinfo: %s" % cpuinfo)
    print("cpuline item 0: %s" % cpuline[0])
    print("memline: %s" % memline)
    print("\n----OS INFO----\n")
    print("sysosline: %s" % sysosline)
    print("sysosid: %s" % sysosid)
    if os.name != "nt":
        print("packagesline item 0: %s" % packagesline[0])
