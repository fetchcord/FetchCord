from fetch_cord.bash import exec_bash, BashError
import sys
import os
import re
from fetch_cord.args import parse_args
from fetch_cord.update import update
from fetch_cord.debugger import run_debug


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

def XDG_Symlink():
    try:
        print("Symlinking XDG_RUNTIME_DIR path for Flatpak Discord.")
        exec_bash(
                "cd %s/.var && ln -sf {app/com.discordapp.Discord,$XDG_RUNTIME_DIR}/discord-ipc-0 " % home)
    except BashError as e:
        print("Could not symlink XDG_RUNTIME_DIR Error: %s" % str(e))
        return

def check_neofetchwin():
    return os.popen("neofetch --noart").read()

def neofetch(loop):
    global cpuline, nvidiagpuline, amdgpuline, termline, fontline, wmline, intelgpuline, radgpuline, \
            vmwaregpuline, virtiogpuline, shell_line, kernelline, sysosline, moboline, \
            deline, batteryline, resline, themeline, hostline, memline, packagesline, diskline,\
            cirrusgpuline
    neofetchwin = False
    if os.name == "nt":
        neofetchwin = check_neofetchwin()
        print(neofetchwin)
    else:
        home = os.getenv('HOME')
        flatpak_discord_path = os.path.isdir("%s/.var/app/com.discordapp.Discord" % home)
        package_path = os.path.isdir("/usr/bin/discord")
        manual_install_path = os.path.isdir("/opt/Discord")
        if loop == 0 and flatpak_discord_path and not package_path and not manual_install_path:
            XDG_Symlink()

        baseinfo = exec_bash("neofetch --stdout")


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
neofetch(loop)


# TODO: move this shit to it's own file
def check_laptop():

    batpath = "/sys/class/power_supply"
    for i in os.listdir(batpath):
        if i.startswith("BAT"):
            return True
    return False


def check_primeoffload(laptop, loop):
    # only show the GPU in use with optimus, show both if prime render offload
    primeoffload = False
    if args.debug and loop == 0:
        print("laptop: %s" % laptop)
    try:
        primeoffload = exec_bash("xrandr --listproviders | grep -o \"NVIDIA-0\"")
        return True
    except BashError:
        return False


def get_nvidia_gpu(nvidiagpuline, loop):
        for n in range(len(nvidiagpuline)):
            nvidiagpuinfo = nvidiagpuline[n]
        try:
            gputemp = exec_bash("nvidia-smi | awk '{print $3}' | xargs | awk '{print $7}' | sed 's/C/°C/;s/^/[/;s/$/]/'")
            nvidiagpuinfo += gputemp
        except BashError:
            pass
        return nvidiagpuinfo


def get_amdgpurender(amdgpuline, intelgpuline, laptop):
    amdgpurenderlist = []
    try:
        # amd GPUs
        for i in range(len(amdgpuline)):
            # assume DRI_PRIME=0 is the intel GPU
            if laptop and intelgpuline:
                i += 1
            env_prime = "env DRI_PRIME=%s" % i
            amdgpurender = "GPU: " + \
                exec_bash(
                    "%s glxinfo | grep \"OpenGL renderer string:\" |\
                            sed 's/^.*: //;s/[(][^)]*[)]//g'" % env_prime) + ' '
            if i != -1:
                amdgpurenderlist.append(amdgpurender)
    except BashError as e:
        print("ERROR: Could not run glxinfo [%s]" % str(e))
        sys.exit(1)
    return amdgpurenderlist

def get_amdgpu(amdgpurenderlist, nvidiagpuline):

    for a in range(len(amdgpurenderlist)):
        if nvidiagpuline:
            amdgpuinfo = '\n' + amdgpurenderlist[a]
        else:
            amdgpuinfo = amdgpurenderlist[a]

    return amdgpuinfo

def get_amdgpu_no_render(amdgpuline):
    for a in range(len(amdgpuline)):
        amdgpuinfo = amdgpuline[a]

    return amdgpuinfo



def get_intelgpu(intelgpuline, primeoffload):

    if amdgpuline or nvidiagpuline:
        intelgpuinfo = '\n' + intelgpuline[0]
    else:
        intelgpuinfo = intelgpuline[0]

    return intelgpuinfo


def get_gpuinfo(cirrusgpuline, vmwaregpuline, virtiogpuline, amdgpuline, nvidiagpuline, intelgpuline, primeoffload):
    if nvidiagpuline:
        gpuinfo = get_nvidia_gpu(nvidiagpuline, loop)

    if amdgpurenderlist and not primeoffload and sysosid.lower() != "macos":
        gpuinfo += get_amdgpu(amdgpurenderlist, nvidiagpuline)

    elif amdgpuline and not amdgpurenderlist and not primeoffload:
        gpuinfo += get_amdgpu_no_render(amdgpuline)

    if intelgpuline and not primeoffload:
        gpuinfo += get_intelgpu(intelgpuline, primeoffload)

    if vmwaregpuline:
        gpuinfo = vmwaregpuline[0]

    if virtiogpuline:
        gpuinfo = virtiogpuline[0]

    if cirrusgpuline:
        gpuinfo = cirrusgpuline[0]

    return gpuinfo


def get_gpu_vendors(cirrusgpuline, vmwaregpuline, virtiogpuline,\
        amdgpuline, nvidiagpuline, intelgpuline, primeoffload, sysosid):

    if nvidiagpuline:
        gpuvendor = "NVIDIA"

    if amdgpuline and not primeoffload:
        gpuvendor += "AMD"

    if intelgpuline and not primeoffload:
        if sysosid.lower() == "macos" and "Radeon" in intelgpuline[0].split():
            gpuvendor += "AMD"
        gpuvendor += "Intel"

    if vmwaregpuline:
        gpuvendor = "vmware"

    if virtiogpuline:
        gpuvendor = "virtio"

    if cirrusgpuline:
        gpuvendor = "cirrus"

    return gpuvendor


def get_win_gpu():
    global gpuinfo, gpuvendor
    gpuinfo = ""
    gpuvendor = ""
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


def get_cpuinfo(cpuline):
    if os.name != "nt":
        cpuinfo = ' '.join([' '.join(cpuline[0].split()[:-2]), cpuline[0].split()[-2].replace(
            "0G", "G", 1), cpuline[0].split()[-1]])

    else:
        cpuinfo = ' '.join(cpuline)
        cpuinfo = re.sub(r"\((.+)\)", "", cpuinfo)
    return cpuinfo


def get_cpumodel(cpuline, cpuvendor):
    if cpuvendor == "Intel":
        if os.name != "nt":
            cpumodel = ' '.join([cpuline[0].replace(
                '-', ' ').split()[1], cpuline[0].replace('-', ' ').split()[2]])
            if cpumodel == "Intel Core":
                cpumodel = cpuline[0].split()[1:5]
                cpumodel = ' '.join(cpumodel)
        else:
            cpumodel = ' '.join([cpuline[0].replace(
                '-', ' ').split()[1], cpuline[0].replace('-', ' ').split()[3]])
            if cpumodel == "Intel 2" or cpumodel == "Intel Solo":
                cpumodel = cpuline[0].split()[1:5]
                cpumodel = ' '.join(cpumodel)

    elif cpuvendor == "AMD":
        cpumodel = ' '.join([cpuline[0].split()[2], cpuline[0].split()[3]])
    # fuck you intel
    elif cpuvendor == "Pentium":
        cpumodel = cpuline[0].split()[1]
    return cpumodel

def check_termid(termline):
    if termline:
        termid = termline[0].split()[1]
    else:
        termid = "N/A"

    return termid


def check_fontline(fontline):
    if fontline:
        fontline = '\n'.join(fontline)
    if fontline and args.termfont:
        print("Custom terminal font not set because a terminal font already exists, %s" %
            fontline)
    elif not fontline:
        fontline = "Terminal Font: N/A\nFont: N/A"

    return fontline


def get_wmid(wmline):
    if wmline:
        wmid = wmline[0].split()[1]
    else:
        wmid = "N/A"
    return wmid


def get_deid(deline):
    if deline:
        deid = deline[0].split()[1]
    else:
        deid = "N/A"

    return deid


def get_dewm(deline, wmline):
    dewmid = ""
    if deline and wmline:
        dewmid = deline[0] + ' ' + wmline[0]
    elif deline and not wmline:
        dewmid = deline[0]
    elif wmline and not deline:
        dewmid = wmline[0]
    else:
        dewmid = "N/A"

    return dewmid


def set_laptop(laptop):
    if laptop and sysosid.lower() != 'macos':
        lapordesk = "laptop"
    else:
        lapordesk = "desktop"

    return lapordesk


def check_res(resline):
    if not resline:
        resline = "Resolution: N/A"
    else:
        resline = resline[0]

    return resline


def check_theme(themeline):
    if not themeline:
        themeline = "Theme: N/A"
    else:
        themeline = '\n'.join(themeline)

    return themeline


def check_memline(memline):
    if memline:
        memline = memline[0]
    if not memline:
        memline = "Memory: N/A"

    return memline


def check_batteryline(batteryline, lapordesk):
    if batteryline:
        batteryline = batteryline[0]
    else:
        batteryline = lapordesk

    return batteryline


def get_long_os(sysosline):

    sysosid = sysosline[0].split()[1] + sysosline[0].split()[2]

    return sysosid

def check_diskline(diskline):
    if diskline:
        diskline = '\n'.join(diskline)
    # return to default line
    elif not diskline:
        diskline = cpuinfo

    return diskline

sysosid = sysosline[0].split()[1]

# I don't know if macOS has the same path linux does to check power_supply
if sysosid.lower() != "macos" and os.name != "nt":
    laptop = check_laptop()

gpuinfo = ""
amdgpurenderlist = []
gpuvendor = ""

if amdgpuline and os.name != "nt":
    amdgpurenderlist = get_amdgpurender(amdgpuline, intelgpuline, laptop)

primeoffload = check_primeoffload(laptop, loop)

if os.name != "nt":
    gpuinfo = get_gpuinfo(cirrusgpuline, vmwaregpuline, virtiogpuline, amdgpuline, nvidiagpuline, intelgpuline, primeoffload)
    gpuvendor = get_gpu_vendors(cirrusgpuline, vmwaregpuline, virtiogpuline, amdgpuline, nvidiagpuline, intelgpuline, primeoffload, sysosid)

else:
    get_win_gpu()


if not hostline:
    hostline = "Host: N/A"
if not kernelline:
    kernelline = "Kernel: N/A"
if not shell_line:
    shell_line = "Shell: N/A"
if not moboline:
    moboline = "Motherboard: N/A"

if sysosid.lower() in ['windows', 'linux', 'opensuse']:
    get_long_os(sysosline)

dewmid = get_dewm(deline, wmline)
deid = get_deid(deline)
wmid = get_wmid(wmline)



lapordesk = set_laptop(laptop)
batteryline = check_batteryline(batteryline, lapordesk)

cpuvendor = cpuline[0].split()[1].replace("Intel(R)", "Intel")
cpumodel = get_cpumodel(cpuline, cpuvendor)
cpuinfo = get_cpuinfo(cpuline)
memline = check_memline(memline)
diskline = check_diskline(diskline)

resline = check_res(resline)

themeline = check_theme(themeline)
fontline = check_fontline(fontline)
termid = check_termid(termline)
shellid = shell_line[0].split()[1]





if args.debug:
    run_debug()
