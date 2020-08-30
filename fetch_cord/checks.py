import os
import sys
import re
from fetch_cord.bash import exec_bash, BashError
from fetch_cord.args import parse_args

args = parse_args()


def check_laptop():

    batpath = "/sys/class/power_supply"
    for i in os.listdir(batpath):
        if i.startswith("BAT"):
            return True
    return False


def check_primeoffload():
    # only show the GPU in use with optimus, show both if prime render offload
    primeoffload = False
    try:
        primeoffload = exec_bash("xrandr --listproviders | grep -o \"NVIDIA-0\"")
        return True
    except BashError:
        return False


def nvidia_gpu_temp(gpuline):

    try:
        gputemp = exec_bash("nvidia-smi -q | awk '/GPU Current Temp/{print $5}'\
                    | sed 's/^/[/;s/$/°C]/'")
        for t in range(len(gpuline)):
            if "NVIDIA" in gpuline[t].split():
                nvidiagpu = gpuline[t] + gputemp
    except BashError:
        pass
    print(nvidiagpu)

    return nvidiagpu


def get_amdgpurender(gpuline, laptop):
    amdgpurenderlist = []
    try:
        # amd GPUs
        for i in range(len(gpuline)):
            # assume DRI_PRIME=0 is the intel GPU
            if laptop and "Intel" in gpuline[i].split():
                i += 1
            env_prime = "env DRI_PRIME=%s" % i
            if "AMD" in gpuline[i].split():
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


def get_amdgpu(amdgpurenderlist, gpuline):
    amdgpuline= ""
    for a in range(len(amdgpurenderlist)):
        if "AMD" not in gpuline[a]:
            amdgpuline += gpuline[a]
        amdgpuline += amdgpurenderlist[a]
    return amdgpuline


def strip_prime(primeoffload, gpuline):
    prime = []
    for p in range(len(gpuline)):
        if "NVIDIA" in gpuline[p].split() and primeoffload:

            prime = gpuline[p]
    return nvidia_gpu_temp(gpuline)

def get_gpuinfo(primeoffload, gpuline, laptop, sysosid, amdgpurenderlist):
    gpuinfo = ""
    if primeoffload and laptop:
        gpuinfo += strip_prime(primeoffload, gpuline)
    if sysosid.lower() not in ["macos", "windows"] and not primeoffload:
        gpuinfo += get_amdgpu(amdgpurenderlist, gpuline)
    for line in range(len(gpuline)):
        if "NVIDIA" in gpuline[line].split() and not primeoffload:
            gpuinfo += nvidia_gpu_temp(gpuline)
    return gpuinfo



def get_gpu_vendors(gpuline, primeoffload, sysosid):

    gpuvendor = ""
    gpujoin = '\n'.join(gpuline)
    if "NVIDIA" in gpujoin.split():
        gpuvendor += "NVIDIA"

    if "AMD" in gpujoin.split() and not primeoffload:
        gpuvendor += "AMD"

    if "Intel" in gpujoin.split() and not primeoffload:
        if sysosid.lower() == "macos" and "Radeon" in gpuline[line].split():
            gpuvendor += "AMD"
        gpuvendor += "Intel"

    if "VMWare" in gpujoin.split():
        gpuvendor = "vmware"

    if "Red Hat" in gpujoin.split():
        gpuvendor = "virtio"

    if "Cirrus" in gpujoin.split():
        gpuvendor = "cirrus"

    return gpuvendor

def get_win_gpu(nvidiagpuline, radgpuline, intelgpuline):
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

    return gpuinfo, gpuvendor


def get_cpuinfo(cpuline, baseinfo):
    if baseinfo:
        cpuinfo = ' '.join([' '.join(cpuline[0].split()[:-2]), cpuline[0].split()[-2].replace(
            "0G", "G", 1), cpuline[0].split()[-1]])

    else:
        cpuinfo = ' '.join(cpuline)
        cpuinfo = re.sub(r"\((.+)\)", "", cpuinfo)
    return cpuinfo


def get_cpumodel(cpuline, cpuvendor, baseinfo):
    if cpuvendor == "Intel":
        if baseinfo:
            cpumodel = ' '.join([cpuline[0].replace(
                '-', ' ').split()[1], cpuline[0].replace('-', ' ').split()[2]])
            if cpumodel == "Intel Core":
                cpumodel = cpuline[0].split()[1:5]
                cpumodel = ' '.join(cpumodel)
        else:
            cpumodel = ' '.join([cpuline[0].replace(
                '-', ' ').split()[1], cpuline[0].replace('-', ' ').split()[3]])
            cpumodel = re.sub(r"\((.+)\)", "", cpumodel)
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


def set_laptop(laptop, sysosid):
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
        memline = ''.join(memline)
    if not memline:
        memline = "Memory: N/A"

    return memline


def check_batteryline(batteryline, hostline):
    if batteryline:
        batteryline = '\n'.join(batteryline)
    else:
        batteryline = ' '.join(hostline)

    return batteryline


def get_long_os(sysosline):

    sysosid = sysosline[0].split()[1] + sysosline[0].split()[2]

    return sysosid

def check_diskline(diskline, cpuinfo):
    if diskline:
        diskline = '\n'.join(diskline)
    # return to default line
    elif not diskline:
        diskline = cpuinfo

    return diskline
