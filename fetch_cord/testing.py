#import shit as usual
import os
from fetch_cord.bash import exec_bash, BashError
from fetch_cord.out import wmid, deid, termid, shellid, cpumodel, cpuvendor, gpuvendor, sysosid
#appid for discord app
appid = "none"
#number of packages
packages = "none"
#find out uptime for epoch time
if not sysosid.lower() == "macos":
    uptime = exec_bash("cat /proc/stat | grep btime | awk '{print $2}'")
# predefine ids
cpuid = "none"
cpuappid = "none"
gpuid = "none"
termappid = "none"
desktopid = "none"
#distros set id and package number
def iUbuntu():
	global appid
	appid='740434138036699178'
def iVoid():
        global appid
        appid='740484961353597039'
def iOpenSuseLeap():
	global appid
	appid='740156532137787433'
def iOpenSuseTumble():
	global appid
	appid='742180413132505088'
def iCentos():
	global appid
	appid='740483295388631071'
def iArch():
	global appid
	appid='740476198437650473'
def iArtix():
        global appid
        appid='741918141248045107'
def iFedora():
	global appid
	appid='740485660703719464'
def iGentoo():
	global appid
	appid='740484380652208140'
def iDebian():
	global appid
	appid='740490017218232392'
def iManjaro():
	global appid
	appid='740614258177605642'
def iLinuxMint():
        global appid
        appid='740633577481568317'
def iLMDE():
        global appid
        appid='741726946588622988'
def iPop():
	global appid
	appid='740660055925587978'
def iEnde():
	global appid
	appid='740809641545564170'
def iWindows10():
        global appid
        appid='741949889465942099'
def iWindows8_1():
        global appid
        appid='741952065294827520'
def iWindows8():
        global appid
        appid='741952179488948324'
def iWindows7():
        global appid
        appid='741952383512346696'
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
if sysosid.lower() == "macos":
    devicetype = "none"
    bigicon = "none"
    ver = os.popen("sw_vers -productVersion").read()
    uptime = os.popen("sysctl -n kern.boottime").read().split()[3]
    product = os.popen("sysctl -n hw.model").read()
    laorp()
#def desktops and defind id
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
#this is to check wether the user is actually using unity
#or using unity as an xdg value to fix issues with electron apps
	if wmid.lower() == "compiz":
		global desktopid
		desktopid = "unity"
	else:
		desktopid = wmid
def iAero():
        global desktopid
        desktopid = "aero"
#window managers
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
# cpuids
def Amdcpu():
        global cpuid, cpuappid
        cpuid = {
        "22": "Jaguar",
        }[cpu]
        cpuappid='740752899054895105'
        return cpuid
def Ryzen():
        global cpuid, cpuappid
        cpuid = "Ryzen"
        cpuappid='740752899054895105'
def Intelcorei3():
        global cpuid, cpuappid
        cpuid = "Intel(R) Core(TM) i3"
        cpuappid='741044208512532570'
def Intelcorei5():
        global cpuid, cpuappid
        cpuid = "Intel(R) Core(TM) i5"
        cpuappid='741099939198926920'
def Intelcorei7():
        global cpuid, cpuappid
        cpuid = "Intel(R) Core(TM) i7"
        cpuappid='741100300219187335'
def Intelcorei9():
        global cpuid, cpuappid
        cpuid = "Intel(R) Core(TM) i9"
        cpuappid='741100622040006719'
def Intelpentium():
        global cpuid, cpuappid
        cpuid = "Intel(R) Pentium(R)"
        cpuappid='741203845706940467'
def Ryzen3():
        global cpuid, cpuappid
        cpuid = "AMD Ryzen 3"
        cpuappid='741153175779803146'
def Ryzen5():
        global cpuid, cpuappid
        cpuid = "AMD Ryzen 5"
        cpuappid='741152732756312125'
def Ryzen7():
        global cpuid, cpuappid
        cpuid = "AMD Ryzen 7"
        cpuappid='740752899054895105'
def Ryzen9():
        global cpuid, cpuappid
        cpuid = "AMD Ryzen 9"
        cpuappid='741152930899427364'
def Ryzenth():
        global cpuid, cpuappid
        cpuid = "AMD Ryzen Threadripper"
        cpuappid='742075019257184338'
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
# terminals
def St():
        global termappid
        termappid='741280043220861030'
def Kitty():
        global termappid
        termappid='741285676250824725'
def Alacritty():
        global termappid
        termappid='741291339945345045'
def Xterm():
        global termappid
        termappid='741287143187546125'
def Konsole():
        global termappid
        termappid='741286819676553258'
def Gnometerminal():
        global termappid
        termappid='741328861115056160'
def Coolretroterm():
        global termappid
        termappid='741731097498353794'
def Fetchcord():
        global termappid
        termappid='742096605502767235'
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
}
gpus = {
    "intel": Intelgpu,
    "nvidia": Nvidiagpu,
    "amd": Amdgpu,
    "radeon": Amdgpu,
    # multi GPUs
    "nvidiaintel": Nvidia_intelgpu,
    "nvidiaamd": Nvidia_amdgpu,
    "amdintel": Amd_intelgpu,
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
}
#desktops
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
terms = {
    "st": St,
    "kitty": Kitty,
    "alacritty": Alacritty,
    "xterm": Xterm,
    "konsole": Konsole,
    "dolphin": Konsole,
    "gnome-terminal": Gnometerminal,
    "cool-retro-term": Coolretroterm,
    "fetchcord": Fetchcord,
}
shells = {
    "fish": Fish,
    "zsh": Zsh,
    "bash": Bash,
}
#bunch of try except blocks to catch keyerrors and tell the enduser that thier distro/others arent supported
try:
	distros[sysosid.lower()]()
except KeyError:
	print("Unsupported Distro, contact me on the GitHub page to resolve this.(keyerror)")

if sysosid == "macos":
    try:
        versions[ver[0:5]]()
    except IndexError:
        bigicon = "bigslurp"
    except KeyError:
        print("Unsupported MacOS version")

try:
    if deid != "none":
        desktops[deid.lower()]()
except KeyError:
	print("Unsupported De contact me on github to resolve this.(Keyerror)")
pass
try:
    if deid == "none":
        windowmanagers[wmid.lower()]()
except KeyError:
        print("Unsupported Wm contact me on github to resolve this.(Keyerror)")
try:
        if cpuvendor == "AMD":
            amdcpus[cpumodel.lower()]()
        elif cpuvendor == "Intel":
            intelcpus[cpumodel.lower()]()
except KeyError:
        print("unknown CPU, contact me on github to resolve this.(Keyerror)")

try:
        gpus[gpuvendor.lower()]()
except KeyError:
        print("Unknown GPU, contact me on github to resolve this.(Keyerror)")
try:
        terms[termid.lower()]()
except KeyError:
        print("Unsupported Terminal. contact me on github to resolve this.(Keyerror)")
try:
        shells[shellid.lower()]()
except KeyError:
        print("Unsupported Shell, contact me on guthub to resolve this.(Keyerror)")
