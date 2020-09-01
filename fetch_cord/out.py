from fetch_cord.bash import exec_bash, BashError
import sys
import os
import re
import subprocess

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources
import fetch_cord.ressources as ressources

import fetch_cord.__init__ as __init__
from fetch_cord.args import parse_args
from fetch_cord.update import update
from fetch_cord.debugger import run_debug
from fetch_cord.checks import get_amdgpurender, check_primeoffload, get_gpu_vendors,\
    set_laptop, check_fontline,\
    get_cpumodel, get_cpuinfo, check_laptop, get_long_os, nvidia_gpu_temp,\
    strip_prime, get_gpuinfo

args = parse_args()

if args.update:
    update()

if args.version:
    print("FetchCord version:", __init__.VERSION)
    sys.exit(0)


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

def check_neofetch_scoop(default_config):
    return subprocess.run(
        [
            "neofetch",
            "--stdout",
            "--config=%s" % "none" if args.noconfig else (
                args.config_path if args.config_path else (default_config))
        ],
        encoding="utf-8",
        stdout=subprocess.PIPE,
        shell=(os.name == "nt")
    ).stdout


def check_neofetchwin():
    return subprocess.run(["neofetch", "--noart"], check=True, encoding='utf-8', stdout=subprocess.PIPE).stdout


def get_default_config():
    with pkg_resources.path(ressources, 'default.conf') as path:
        return path

    return None

def neofetch(loop):
    neofetchwin = False
    if os.name == "nt":
        try:
            neofetchwin = check_neofetchwin()
        except (FileNotFoundError, subprocess.CalledProcessError) as e:
            pass

        if not neofetchwin:
            try:
                baseinfo = check_neofetch_scoop(get_default_config())
            except (FileNotFoundError, subprocess.CalledProcessError) as e:
                print(
                    "ERROR: Neofetch not found, please install it or check installation and that neofetch is in PATH.")
                sys.exit(1)
    else:
        home = os.getenv('HOME')
        flatpak_discord_path = os.path.isdir(
            "%s/.var/app/com.discordapp.Discord" % home)
        package_path = os.path.isfile("/usr/bin/discord")
        manual_install_path = os.path.isdir("/opt/Discord")
        default_config = ''.join([os.path.dirname(__file__), "/ressources/default.conf"])
        if loop == 0 and flatpak_discord_path and not package_path and not manual_install_path:
            XDG_Symlink(home)
        try:
            baseinfo = check_neofetch_scoop(default_config)
        except (FileNotFoundError, subprocess.CalledProcessError) as e:
            print("ERROR: Neofetch not found, please install it or check installation and that neofetch is in PATH.")
            sys.exit(1)

    # make lists
    cpu = "CPU:"
    cpuline = []
    gpu = "GPU:"
    gpuline = []
    radgpu = "Radeon"
    nvidiagpu = "NVIDIA"
    radgpuline = []
    term = "Terminal:"
    termline = []
    font = "Font:"
    fontline = []
    wm = "WM:"
    wmline = []
    disk = "Disk"
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
    hostline = []
    res = "Resolution:"
    resline = []
    theme = "Theme:"
    themeline = []
    battery = "Battery"
    batteryline = []

    filepath = "tmp.txt"
    with open(filepath, 'w') as f:
        print(baseinfo, file=f)
    with open(filepath, "rt") as f:
        lines = f.readlines()
        for i in range(len(lines)):
            line = lines[i]
            if line.find(cpu) != -1:
                cpuline.append(line.rstrip('\n'))
            if line.find(gpu) != -1:
                gpuline.append(line.rstrip('\n'))
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
                    memline.append(' '.join(
                        ["Memory:", str(round(used / 1024, 2)), "GiB /", str(
                            round(total / 1024, 2)), "GiB"]))
            elif line.find(mem) != -1:
                memline.append(line.rstrip('\n'))
            if line.find(theme) != -1:
                themeline.append(line.rstrip('\n'))
            if line.find(disk) != -1 and os.name != "nt":
                diskline.append(line.rstrip('\n'))
            if line.find(battery) != -1:
                batteryline.append(line.rstrip('\n'))
            if neofetchwin:
                if line.find(nvidiagpu) != -1:
                    gpuline.append('',join(["GPU:",
                        line[line.find(nvidiagpu):]]).rstrip('\n'))
                if line.find(radgpu) != -1:
                    gpuline.append(''.join(["GPU:",  line[line.find(radgpu):]]).rstrip('\n'))
                if line.find(disk) != -1:
                    diskline.append(line[line.find(disk):].rstrip('\n'))
                    i += 1
                    while(i < len(lines)):
                        line = lines[i]
                        if line != "\n":
                            diskline.append(''.join([
                                "Disk:", line.lstrip()]).rstrip('\n'))
                        i += 1
                    break


    if not cpuline:
        cpuline = ["CPU: N/A"]
    if not gpuline:
        gpuline = ["GPU: N/A"]
    if not termline:
        termline = ["Terminal: N/A"]
    if not fontline:
        fontline = ["Font: N/A"]
    if not deline:
        deline = ["DE: N/A"]
    if not wmline:
        wmline = ["WM: N/A"]
    if not shell_line:
        shell_line = ["Shell: N/A"]
    if not packagesline:
        packagesline = ["Packages: N/A"]
    if not kernelline:
        kernelline = ["Kernel: N/A"]
    if not sysosline:
        sysosline = ["OS: N/A"]
    if not hostline:
        hostline = ["Host: N/A"]
    if not resline:
        resline = ["Resolution: N/A"]
    if not memline:
        memline = ["Memory: N/A"]
    if not themeline:
        themeline = ["Theme: N/A"]
    if not diskline:
        diskline = ["Disk: N/A"]
    if not batteryline:
        batteryline = ["Battery: N/A"]
    if not moboline:
        moboline = ["Motherboard: N/A"]

    try:
        if os.path.isfile(filepath):
            os.remove(filepath)
    except FileNotFoundError:
        pass

    return cpuline, gpuline, termline, fontline, wmline, radgpuline, \
        shell_line, kernelline, sysosline, moboline, neofetchwin,\
        deline, batteryline, resline, themeline, hostline, memline, packagesline, diskline


cpuline, gpuline, termline, fontline, wmline, radgpuline, \
    shell_line, kernelline, sysosline, moboline, neofetchwin,\
    deline, batteryline, resline, themeline, hostline, memline, packagesline, diskline = neofetch(loop)

sysosid = sysosline[0].split()[1]
# I don't know if macOS has the same path linux does to check power_supply
if sysosid.lower() != "macos" and os.name != "nt":
    laptop = check_laptop()
else:
    laptop = False

amdgpurenderlist = []
gpuvendor = ""
for line in range(len(gpuline)):
    if "AMD" in gpuline[line].split() and os.name != "nt":
        amdgpurenderlist = get_amdgpurender(gpuline, laptop)
        break
if sysosid.lower() not in ["windows", "macos"]:
    primeoffload = check_primeoffload()
else:
    primeoffload = False

gpuinfo = get_gpuinfo(primeoffload, gpuline, laptop,
                        sysosid, amdgpurenderlist)
gpuvendor = get_gpu_vendors(gpuline, primeoffload, sysosid)

dewmid = '\n'.join(deline + wmline)
deid = deline[0].split()[1]
wmid = wmline[0].split()[1]

lapordesk = set_laptop(laptop, sysosid)
batteryline = '\n'.join(batteryline)
resline = ''.join(resline)

packagesline = ''.join(packagesline)
kernelline = ''.join(kernelline)

themeline = ''.join(themeline)
fontline = check_fontline(fontline)

termid = termline[0].split()[1]

shellid = shell_line[0].split()[1]
shell_line = ''.join(shell_line)

termline = ''.join(termline)
sysosline = ''.join(sysosline)
hostline = ''.join(hostline)
memline = ''.join(memline)
moboline = ''.join(moboline)

if sysosid.lower() in ['windows', 'linux', 'opensuse']:
    sysosid = get_long_os(sysosline)


cpuvendor = cpuline[0].split()[1].replace("Intel(R)", "Intel")
cpumodel = get_cpumodel(cpuline, cpuvendor)
cpuinfo = get_cpuinfo(cpuline)
memline = ''.join(memline)
diskline = '\n'.join(diskline)

if args.debug:
    run_debug()
