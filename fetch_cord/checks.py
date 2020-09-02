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
            break
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
    nvidiagpu = ""

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
        gpuinfo = strip_prime(primeoffload, gpuline)

    if sysosid.lower() not in ["macos", "windows"] and not primeoffload:
        gpuinfo += get_amdgpu(amdgpurenderlist, gpuline)

    for line in range(len(gpuline)):
        if "NVIDIA" in gpuline[line].split() and not primeoffload:
            try:
                gpuinfo += '\n' + nvidia_gpu_temp(gpuline[line])
            except BashError as e:
                print("Cannot get Nvidia gpu temp: "+e)
                gpuinfo += '\n' +gpuline[line]

    return gpuinfo


def get_gpu_vendors(gpuline, primeoffload, sysosid):

    gpuvendor = []
    for vendor in range(len(gpuline)):
        if gpuline[vendor].split() not in gpuvendor:
            gpuvendor.append(gpuline[vendor].split()[1])
    gpuvendor = ''.join(gpuvendor)

    return gpuvendor


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
            cpumodel = re.sub(r"\((.+)\)", "", cpumodel)
            if cpumodel == "Intel 2" or cpumodel == "Intel Solo":
                cpumodel = cpuline[0].split()[1:5]
                cpumodel = ' '.join(cpumodel)

    elif cpuvendor == "AMD":
        cpumodel = ' '.join([cpuline[0].split()[2], cpuline[0].split()[3]])
    # fuck you intel
    elif cpuvendor == "Pentium":
        cpumodel = cpuline[0].split()[1]
    else:
        cpumodel = "N/A"
    return cpumodel


def check_fontline(fontline):
    if fontline and args.termfont:
        print("Custom terminal font not set because a terminal font already exists, %s" %
            fontline)

    return fontline


def set_laptop(laptop, sysosid):
    if laptop and sysosid.lower() != 'macos':
        lapordesk = "laptop"
    else:
        lapordesk = "desktop"

    return lapordesk


def get_long_os(sysosline):
    sysosid = sysosline.split()[1] + sysosline.split()[2]

    return sysosid
