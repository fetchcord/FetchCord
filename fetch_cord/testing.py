# import shit as usual
import os
from fetch_cord.args import parse_args
from fetch_cord.bash import exec_bash
from fetch_cord.out import wmid, deid, termid, shellid, cpumodel, cpuvendor, gpuvendor, sysosid, hostid

# appid for discord app
appid = "none"

# number of packages
packages = "none"

# find out uptime for epoch time
uptime = ""
if not sysosid.lower() == "macos":
    uptime = exec_bash("cat /proc/stat | grep btime | awk '{print $2}'")
if sysosid.lower() in ["windows10", "windows7", "windows8", "windows8.1"]:
    uptime = os.popen("wmic os get lastbootuptime").read()

# predefine ids
cpuid = "none"
cpuappid = "none"
gpuid = "none"
termappid = "none"
desktopid = "none"
hostappid = "none"

# distros set id and package number


def iUbuntu():
    global appid
    appid = '740434138036699178'


def iVoid():
    global appid
    appid = '740484961353597039'


def iOpenSuseLeap():
    global appid
    appid = '740156532137787433'


def iOpenSuseTumble():
    global appid
    appid = '742180413132505088'


def iCentos():
    global appid
    appid = '740483295388631071'


def iArch():
    global appid
    appid = '740476198437650473'


def iArtix():
    global appid
    appid = '741918141248045107'


def iFedora():
    global appid
    appid = '740485660703719464'


def iGentoo():
    global appid
    appid = '740484380652208140'


def iDebian():
    global appid
    appid = '740490017218232392'


def iManjaro():
    global appid
    appid = '740614258177605642'


def iLinuxMint():
    global appid
    appid = '740633577481568317'


def iLMDE():
    global appid
    appid = '741726946588622988'


def iPop():
    global appid
    appid = '740660055925587978'


def iEnde():
    global appid
    appid = '740809641545564170'


def iNixOS():
    global appid
    appid = '742887089179197462'


def iWindows10():
    global appid
    appid = '741949889465942099'


def iWindows8_1():
    global appid
    appid = '741952065294827520'


def iWindows8():
    global appid
    appid = '741952179488948324'


def iWindows7():
    global appid
    appid = '741952383512346696'


def Unknown_distro():
    global appid
    appid = '742887089179197462'

# MacOS versions


def iHsiera():
    global bigicon
    bigicon = "hsierria"


def iMojave():
    global bigicon
    bigicon = "mojave"


def iCatilina():
    global bigicon
    bigicon = "catilina"

# macOS hardwawre


def laporp():
    global devicetype
    if product[0:7] == "MacBook":
        devicetype = "laptop"
    else:
        devicetype = "desktop"

def macos():
    global product, bigicon, ver, uptime
    if sysosid.lower() == "macos":
        devicetype = "none"
        bigicon = "none"
        ver = os.popen("sw_vers -productVersion").read()
        uptime = os.popen("sysctl -n kern.boottime").read().split()[3]
        product = os.popen("sysctl -n hw.model").read()
        laporp()

# def desktops and defind id


def iKde():
    global desktopid
    desktopid = "kde"


def iGnome():
    global desktopid
    desktopid = "gnome"


def iXfce():
    global desktopid
    desktopid = "xfce"


def iCinnamon():
    global desktopid
    desktopid = "cinnamon"


def iBudgie():
    global desktopid
    desktopid = "budgie"


def iDeepin():
    global desktopid
    desktopid = "deepin"


def iMate():
    global desktopid
    desktopid = "mate"


def iUnity():
    # this is to check wether the user is actually using unity
    # or using unity as an xdg value to fix issues with electron apps
    if wmid.lower() == "compiz":
        global desktopid
        desktopid = "unity"
    else:
        desktopid = wmid


def iAero():
    global desktopid
    desktopid = "aero"

# window managers


def iDwm():
    global desktopid
    desktopid = "dwm"


def iAwesome():
    global desktopid
    desktopid = "awesome"


def Ii3():
    global desktopid
    desktopid = "i3"


def iEnlightenment():
    global desktopid
    desktopid = "enlightenment"


def iXmonad():
    global desktopid
    desktopid = "xmonad"


def iBspwm():
    global desktopid
    desktopid = "bspwm"

def iSway():
    global desktopid
    desktopid = "sway"


def Unknown_de_wm():
    global desktopid
    desktopid = 'unknown'

# cpuids


def Ryzen():
    global cpuid, cpuappid
    cpuid = "Ryzen"
    cpuappid = '740752899054895105'


def Intelcorei3():
    global cpuid, cpuappid
    cpuid = "Intel(R) Core(TM) i3"
    cpuappid = '741044208512532570'


def Intelcorei5():
    global cpuid, cpuappid
    cpuid = "Intel(R) Core(TM) i5"
    cpuappid = '741099939198926920'


def Intelcorei7():
    global cpuid, cpuappid
    cpuid = "Intel(R) Core(TM) i7"
    cpuappid = '741100300219187335'


def Intelcorei9():
    global cpuid, cpuappid
    cpuid = "Intel(R) Core(TM) i9"
    cpuappid = '741100622040006719'


def Intelpentium():
    global cpuid, cpuappid
    cpuid = "Intel(R) Pentium(R)"
    cpuappid = '741203845706940467'


def Intelceleron():
    global cpuid, cpuappid
    cpuid = "Intel(R) Celeron(R)"
    cpuappid = '742904581360713849'


def Ryzen3():
    global cpuid, cpuappid
    cpuid = "AMD Ryzen 3"
    cpuappid = '741153175779803146'


def Ryzen5():
    global cpuid, cpuappid
    cpuid = "AMD Ryzen 5"
    cpuappid = '741152732756312125'


def Ryzen7():
    global cpuid, cpuappid
    cpuid = "AMD Ryzen 7"
    cpuappid = '740752899054895105'


def Ryzen9():
    global cpuid, cpuappid
    cpuid = "AMD Ryzen 9"
    cpuappid = '741152930899427364'


def Ryzenth():
    global cpuid, cpuappid
    cpuid = "AMD Ryzen Threadripper"
    cpuappid = '742075019257184338'


def Unknown_cpu():
    global cpuid, cpuappid
    cpuid = "Unknown CPU"
    cpuappid = '742887089179197462'

# gpuids


def Intelgpu():
    global gpuid
    gpuid = "intel"


def Nvidiagpu():
    global gpuid
    gpuid = "nvidia"


def Nvidia_intelgpu():
    global gpuid
    gpuid = "nvidia-intel"


def Nvidia_amdgpu():
    global gpuid
    gpuid = "nvidia-amd"


def Amdgpu():
    global gpuid
    gpuid = "amd"


def Amd_intelgpu():
    global gpuid
    gpuid = "amd-intel"


def Nvidia_amd_intelgpu():
    # again, why
    global gpuid
    gpuid = "nvidia-amd-intel"


def Vmwaregpu():
    global gpuid
    gpuid = "vmware"


def Virtiogpu():
    global gpuid
    gpuid = "virtio"


def Unknown_gpu():
    global gpuid
    gpuid = 'unknown'
# terminals


def St():
    global termappid
    termappid = '741280043220861030'


def Kitty():
    global termappid
    termappid = '741285676250824725'


def Alacritty():
    global termappid
    termappid = '741291339945345045'


def Xterm():
    global termappid
    termappid = '741287143187546125'


def Konsole():
    global termappid
    termappid = '741286819676553258'


def Gnometerminal():
    global termappid
    termappid = '741328861115056160'


def Coolretroterm():
    global termappid
    termappid = '741731097498353794'

def Urxvt():
    global termappid
    termappid = '743246048968835092'


def Fetchcord():
    global termappid
    termappid = '742096605502767235'


def Unknown_term():
    global termappid
    termappid = '742887089179197462'
# shells


def Fish():
    global shell
    shell = "fish"


def Zsh():
    global shell
    shell = "zsh"


def Bash():
    global shell
    shell = "bash"


def Unknown_shell():
    global shell
    shell = "unknown"


# hosts


def iAsus():
    global hostappid
    hostappid = "743936082780880928"


def iDell():
    global hostappid
    hostappid = "743970870631858288"

def iHP():
    global hostappid
    hostappid = "743971270395297852"

def Unknown_host():
    global hostappid
    hostappid = "742887089179197462"


amdcpus = {
    "ryzen 3": Ryzen3,
    "ryzen 5": Ryzen5,
    "ryzen 7": Ryzen7,
    "ryzen 9": Ryzen9,
    "ryzen threadripper": Ryzenth,
}
intelcpus = {
    "intel i3": Intelcorei3,
    "intel i5": Intelcorei5,
    "intel i7": Intelcorei7,
    "intel i9": Intelcorei9,
    "intel pentium": Intelpentium,
    "intel celeron": Intelceleron,
    "pentium": Intelpentium,
}
gpus = {
    "intel": Intelgpu,
    "nvidia": Nvidiagpu,
    "amd": Amdgpu,
    "radeon": Amdgpu,
    "vmware": Vmwaregpu,
    "virtio": Virtiogpu,
    # multi GPUs
    "nvidiaintel": Nvidia_intelgpu,
    "nvidiaamd": Nvidia_amdgpu,
    "amdintel": Amd_intelgpu,
    "radeonintel": Amd_intelgpu,
    "nvidiaamdintel": Nvidia_amd_intelgpu,
}
distros = {
    "ubuntu": iUbuntu,
    "opensuseleap": iOpenSuseLeap,
    "arch": iArch,
    "artix": iArch,
    "fedora": iFedora,
    "void": iVoid,
    "gentoo": iGentoo,
    "centos": iCentos,
    "debian": iDebian,
    "opensusetumbleweed": iOpenSuseTumble,
    "manjaro": iManjaro,
    "linuxmint": iLinuxMint,
    "lmde": iLMDE,
    "pop!_os": iPop,
    "endeavouros": iEnde,
    "artix": iArtix,
    "windows10": iWindows10,
    "windows7": iWindows7,
    "windows8": iWindows8,
    "windows8.1": iWindows8_1,
    "nixos": iNixOS,
}
versions = {
    "10.13": iHsiera,
    "10.14": iMojave,
    "10.15": iCatilina
}
# window managers
windowmanagers = {
    "dwm": iDwm,
    "i3": Ii3,
    "awesome": iAwesome,
    "enlightenment": iEnlightenment,
    "bspwm": iBspwm,
    "xmonad": iXmonad,
    "sway": iSway,
}
# desktops
desktops = {
    "kde": iKde,
    "plasma": iKde,
    "xfce": iXfce,
    "budgie": iBudgie,
    "gnome": iGnome,
    "deepin": iDeepin,
    "cinnamon": iCinnamon,
    "mate": iMate,
    "unity": iUnity,
    "aero": iAero,
}
terminals = {
    "st": St,
    "kitty": Kitty,
    "alacritty": Alacritty,
    "xterm": Xterm,
    "konsole": Konsole,
    "dolphin": Konsole,
    "gnome-terminal": Gnometerminal,
    "cool-retro-term": Coolretroterm,
    "urxvt": Urxvt,
}
shells = {
    "fish": Fish,
    "zsh": Zsh,
    "bash": Bash,
}
hosts= {
    "inspiron": iDell,
    "hp": iHP,
    "tuf": iAsus,
}
# bunch of try except blocks to catch keyerrors and tell the enduser that thier distro/others arent supported
try:
    if sysosid.lower() != "macos":
        distros[sysosid.lower()]()
    elif sysosid.lower() == "macos":
        macos()
except KeyError:
    print("Unsupported Distro, contact me on the GitHub page to resolve this.(keyerror)")
    Unknown_distro()

if sysosid == "macos":
    try:
        versions[ver[0:5]]()
    except IndexError:
        bigicon = "bigslurp"
    except KeyError:
        print("Unsupported MacOS version")

try:
    if deid != "N/A":
        desktops[deid.lower()]()
except KeyError:
    print("Unsupported De contact me on github to resolve this.(Keyerror)")
    Unknown_de_wm()

try:
    if deid == "N/A":
        windowmanagers[wmid.lower()]()
except KeyError:
    print("Unsupported Wm contact me on github to resolve this.(Keyerror)")
    Unknown_de_wm()
try:
    if cpuvendor == "AMD":
        amdcpus[cpumodel.lower()]()
    elif cpuvendor in ["Intel", "Pentium"]:
        intelcpus[cpumodel.lower()]()
except KeyError:
    print("unknown CPU, contact me on github to resolve this.(Keyerror)")
    Unknown_cpu()

try:
    gpus[gpuvendor.lower()]()
except KeyError:
    print("Unknown GPU, contact me on github to resolve this.(Keyerror)")
    Unknown_gpu()

try:
    terminals[termid.lower()]()
except KeyError:
    print("Unsupported Terminal. contact me on github to resolve this.(Keyerror)")
    Unknown_term()

try:
    shells[shellid.lower()]()
except KeyError:
    print("Unsupported Shell, contact me on guthub to resolve this.(Keyerror)")
    Unknown_shell()
try:
    if hostid != "" and sysosid.lower() != "macos":
        hosts[hostid.lower()]()
except KeyError:
    print("Unknown Host, contact us on github to resolve this.(Keyerror)")
    Unknown_host()
args = parse_args()

if args.debug:
    print("testing")
    print("deid: %s" % deid)
    print("wmid: %s" % wmid)
    print("cpumodel: %s" % cpumodel)
    print("gpuvendor: %s" % gpuvendor)
    print("termid: %s" % termid)
    print("shellid: %s" % shellid)
    print("hostid: %s" % hostid)
