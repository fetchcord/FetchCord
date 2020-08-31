from fetch_cord.bash import exec_bash, BashError
import sys
import os
import re
import subprocess
import fetch_cord.__init__ as __init__
from fetch_cord.args import parse_args
from fetch_cord.update import update
from fetch_cord.debugger import run_debug
from fetch_cord.checks import get_amdgpurender, check_primeoffload, get_gpu_vendors, get_dewm, get_deid,\
    get_wmid, set_laptop, check_batteryline, check_theme, check_fontline, check_termid, check_res,\
    get_cpumodel, get_cpuinfo, check_memline, check_diskline, check_laptop, get_long_os, nvidia_gpu_temp,\
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
                args.config_path if args.config_path else default_config)
        ],
        encoding="utf-8",
        stdout=subprocess.PIPE,
        shell=(os.name == "nt")
    ).stdout

def check_neofetchwin():
    return subprocess.run(["neofetch", "--noart"], check=True, encoding='utf-8', stdout=subprocess.PIPE).stdout


def get_default_config():
    try:
        import importlib.resources as pkg_resources
    except ImportError:
        # Try backported to PY<37 `importlib_resources`.
        import importlib_resources as pkg_resources
    import fetch_cord.ressources as ressources

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
        default_config = os.path.dirname(__file__) + "/ressources/default.conf"
        if loop == 0 and flatpak_discord_path and not package_path and not manual_install_path:
            XDG_Symlink(home)
        try:
            baseinfo = check_neofetch_scoop(default_config)
            print(os.name)
        except (FileNotFoundError, subprocess.CalledProcessError) as e:
            print("ERROR: Neofetch not found, please install it or check installation and that neofetch is in PATH.")
            sys.exit(1)

    # make lists
    cpu = "CPU:"
    cpuline = []
    gpu = "GPU:"
    gpuline = []
    term = "Terminal:"
    termline = []
    font = "Font:"
    fontline = []
    wm = "WM:"
    wmline = []
    disk = "Disk:"
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
    battery = "Battery:"
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
                if line.find(sysos) != -1:
                    sysosline.append(line.rstrip('\n'))
                if line.find(mem) != -1:
                    memline.append(line.rstrip('\n'))
                if line.find(mobo) != -1:
                    moboline.append(line.rstrip('\n'))
                if line.find(gpu) != -1:
                    gpuline.append(line[line.find(gpu):].rstrip('\n'))
                if line.find(disk) != -1:
                    diskline.append(line[line.find(disk):].rstrip('\n'))
                    i += 1
                    while(i < len(lines)):
                        line = lines[i]
                        if line != "\n":
                            diskline.append(
                                "Disk: "+line.lstrip().rstrip('\n'))
                        i += 1
                    break

    elif not neofetchwin:
        filepath = "tmp.txt"
        with open(filepath, 'w') as f:
            print(baseinfo, file=f)
        with open(filepath, "rt") as f:
            for line in f:
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
                    memline.append(
                        "Memory: " + str(round(used / 1024, 2)) + "GiB / " + str(
                            round(total / 1024, 2)) + "GiB")
                elif line.find(mem) != -1:
                    memline.append(line.rstrip('\n'))
                if line.find(theme) != -1:
                    themeline.append(line.rstrip('\n'))
                if line.find(disk) != -1:
                    diskline.append(line.rstrip('\n'))
                if line.find(battery) != -1:
                    batteryline.append(line.rstrip('\n'))

    try:
        if os.path.isfile(filepath):
            os.remove(filepath)
    except FileNotFoundError:
        pass

    if not neofetchwin:
        radgpuline = False

    return cpuline, gpuline, termline, fontline, wmline, radgpuline, \
        shell_line, kernelline, sysosline, moboline, \
        deline, batteryline, resline, themeline, hostline, memline, packagesline, diskline,\
        baseinfo, neofetchwin


baseinfo = False
neofetchwin = False

cpuline, gpuline, termline, fontline, wmline, radgpuline, \
    shell_line, kernelline, sysosline, moboline, \
    deline, batteryline, resline, themeline, hostline, memline, packagesline, diskline,\
    baseinfo, neofetchwin = neofetch(loop)

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


if baseinfo:
    gpuinfo = get_gpuinfo(primeoffload, gpuline, laptop,
                          sysosid, amdgpurenderlist)
#    print(gpuline)
    gpuvendor = get_gpu_vendors(gpuline, primeoffload, sysosid)

    if not hostline:
        hostline = ["Host: N/A"]

    if not kernelline:
        kernelline = ["Kernel: N/A"]

    if not shell_line:
        shell_line = ["Shell: N/A"]

    if not packagesline:
        packagesline = ["Packages: N/A"]

    dewmid = get_dewm(deline, wmline)
    deid = get_deid(deline)
    wmid = get_wmid(wmline)

    lapordesk = set_laptop(laptop, sysosid)
    batteryline = check_batteryline(batteryline, hostline)

    themeline = check_theme(themeline)
    fontline = check_fontline(fontline)

    termid = check_termid(termline)

    if not termline:
        termline = ["Terminal: N/A"]

    shellid = shell_line[0].split()[1]

    resline = check_res(resline)

elif neofetchwin:

    if not moboline:
        moboline = "Motherboard: N/A"
    gpuinfo, gpuvendor = get_win_gpu(nvidiagpuline, radgpuline, intelgpuline)
    deid = False
    wmid = False
    termid = False
    hostline = False


if sysosid.lower() in ['windows', 'linux', 'opensuse']:
    sysosid = get_long_os(sysosline)

cpuvendor = cpuline[0].split()[1].replace("Intel(R)", "Intel")
cpumodel = get_cpumodel(cpuline, cpuvendor, baseinfo)
cpuinfo = get_cpuinfo(cpuline, baseinfo)
memline = check_memline(memline)
diskline = check_diskline(diskline, cpuinfo)


if args.debug:
    run_debug()
