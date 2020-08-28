from fetch_cord.bash import exec_bash, BashError
import sys
import os
import re
import subprocess
from fetch_cord.args import parse_args
from fetch_cord.update import update
from fetch_cord.debugger import run_debug
from fetch_cord.checks import get_amdgpurender, check_primeoffload, get_gpuinfo, get_gpu_vendors, get_dewm, get_deid,\
        get_wmid, set_laptop, check_batteryline, check_theme, check_fontline, check_termid, check_res, get_win_gpu,\
        get_cpumodel, get_cpuinfo, check_memline, check_diskline, check_laptop, get_long_os


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

loop = 0

def XDG_Symlink(home):
    try:
        print("Symlinking XDG_RUNTIME_DIR path for Flatpak Discord.")
        exec_bash(
                "cd %s/.var && ln -sf {app/com.discordapp.Discord,$XDG_RUNTIME_DIR}/discord-ipc-0 " % home)
    except BashError as e:
        print("Could not symlink XDG_RUNTIME_DIR Error: %s" % str(e))
        return

def check_neofetch_scoop():
    return subprocess.run(["neofetch", "--stdout"], check=True, encoding='utf-8', stdout=subprocess.PIPE).stdout

def check_neofetchwin():
    return subprocess.run(["neofetch", "--noart"], check=True, encoding='utf-8', stdout=subprocess.PIPE).stdout


def neofetch(loop):
    global cpuline, nvidiagpuline, amdgpuline, termline, fontline, wmline, intelgpuline, radgpuline, \
            vmwaregpuline, virtiogpuline, shell_line, kernelline, sysosline, moboline, \
            deline, batteryline, resline, themeline, hostline, memline, packagesline, diskline,\
            cirrusgpuline, baseinfo, neofetchwin
    neofetchwin = False
    if os.name == "nt":
        try:
            neofetchwin = check_neofetchwin()
        except (FileNotFoundError, subprocess.CalledProcessError) as e:
            pass

        if neofetchwin == False:
            try:
                baseinfo = check_neofetch_scoop()
            except (FileNotFoundError, subprocess.CalledProcessError) as e:
                print("ERROR: Neofetch not found, please install it or check installation and that neofetch is in PATH.")
                sys.exit(1)

    else:
        home = os.getenv('HOME')
        flatpak_discord_path = os.path.isdir("%s/.var/app/com.discordapp.Discord" % home)
        package_path = os.path.isfile("/usr/bin/discord")
        manual_install_path = os.path.isdir("/opt/Discord")
        if loop == 0 and flatpak_discord_path and not package_path and not manual_install_path:
            XDG_Symlink(home)
        try:
            baseinfo = exec_bash("neofetch --stdout")
        except FileNotFoundError:
            print("ERROR: Neofetch not found, please install it or check installation and that neofetch is in PATH.")
            sys.exit(1)



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
    cirrusgpu = "GPU: 00:02.0 Cirrus"
    cirrusgpuline = []
    term = "Terminal:"
    termline = []
    font = "Font:"
    fontline = []
    wm = "WM:"
    wmline = []
    disk  =  "Disk"
    diskline = []
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
    battery = "Battery"
    batteryline = []

    if neofetchwin:
        nvidiagpu = "NVIDIA"
        radgpu = "Radeon"
        intelgpu = "Intel"
        radgpuline = []
        filepath = "tmp.txt"

        with open(filepath, 'w') as f:
            print(neofetchwin, file=f)

        with open(filepath, 'rt') as f:
            lines = f.readlines()
            for i in range(len(lines)):
                line = lines[i]
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
                if line.find(disk) != -1:
                    diskline.append(line[line.find(disk):].rstrip('\n'))
                    i+=1
                    while(i < len(lines)):
                        line = lines[i]
                        if line != "\n":
                            diskline.append("Disk: "+line.lstrip().rstrip('\n'))
                        i+=1
                    break

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
                if line.find(font) != -1:
                    fontline.append(line.rstrip('\n'))
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
                if line.find(mem) != -1 and args.memtype == "gb":
                    memgb = line.rstrip('\n')
                    memgb = memgb.split()
                    used = float(memgb[1].replace("MiB", ""))
                    total = float(memgb[3].replace("MiB", ""))
                    memline.append(
                            "Memory: " + str(round(used / 1024, 2)) + "GiB / " + str(
                                round(total / 1024,2)) + "GiB")
                elif line.find(mem) != -1:
                    memline.append(line.rstrip('\n'))
                if line.find(theme) != -1:
                    themeline.append(line.rstrip('\n'))
                if line.find(disk) != -1:
                    diskline.append(line.rstrip('\n'))
                if line.find(battery) != -1:
                    batteryline.append(line.rstrip('\n'))
                if line.find(cirrusgpu) != -1:
                    cirrusgpuline.append(line.rstrip('\n'))

    try:
        if os.path.isfile(filepath):
            os.remove(filepath)
    except FileNotFoundError:
        pass

    return (memline, packagesline, diskline, batteryline, cpuline)

baseinfo = False
neofetchwin = False
neofetch(loop)

sysosid = sysosline[0].split()[1]

# I don't know if macOS has the same path linux does to check power_supply
if sysosid.lower() != "macos" and os.name != "nt":
    laptop = check_laptop()
else:
    laptop = False

gpuinfo = ""
amdgpurenderlist = []
gpuvendor = ""


if amdgpuline and os.name != "nt":
    amdgpurenderlist = get_amdgpurender(amdgpuline, intelgpuline, laptop)
if sysosid.lower() not in ["windows", "macos"]:
    primeoffload = check_primeoffload(laptop, loop)
else:
    primeoffload = False


if os.name != "nt" or baseinfo:
    gpuinfo = get_gpuinfo(cirrusgpuline, vmwaregpuline, virtiogpuline, amdgpuline, nvidiagpuline,\
            intelgpuline, primeoffload, amdgpurenderlist, sysosid, loop)
    gpuvendor = get_gpu_vendors(cirrusgpuline, vmwaregpuline, virtiogpuline, amdgpuline,\
            nvidiagpuline, intelgpuline, primeoffload, sysosid)

    dewmid = get_dewm(deline, wmline)
    deid = get_deid(deline)
    wmid = get_wmid(wmline)

    lapordesk = set_laptop(laptop, sysosid)
    batteryline = check_batteryline(batteryline, hostline)

    themeline = check_theme(themeline)
    fontline = check_fontline(fontline)
    termid = check_termid(termline)
    shellid = shell_line[0].split()[1]

    resline = check_res(resline)

elif neofetchwin and os.name == "nt":
    gpuinfo, gpuvendor = get_win_gpu(nvidiagpuline, radgpuline, intelgpuline)
    deid = False
    wmid = False
    termid = False



if not hostline:
    hostline = "Host: N/A"
if not kernelline:
    kernelline = "Kernel: N/A"
if not shell_line:
    shell_line = "Shell: N/A"
if not moboline:
    moboline = "Motherboard: N/A"
if not gpuinfo:
    gpuinfo = "GPU: N/A"
if not termline:
    termline = "Terminal: N/A"
if not packagesline:
    packagesline= "Packages: N/A"

if sysosid.lower() in ['windows', 'linux', 'opensuse']:
    sysosid = get_long_os(sysosline)

cpuvendor = cpuline[0].split()[1].replace("Intel(R)", "Intel")
cpumodel = get_cpumodel(cpuline, cpuvendor, baseinfo)
cpuinfo = get_cpuinfo(cpuline, baseinfo)
memline = check_memline(memline)
diskline = check_diskline(diskline, cpuinfo)


if args.debug:
    run_debug()
