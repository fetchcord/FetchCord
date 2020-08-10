import distro
import os
from .bash import exec_bash, BashError
from .out import cpu, wmid, deid, termid, shellid, cpumodel, cpuvendor, gpuvendor, sysosid
info = distro.linux_distribution(full_distribution_name=False)
ldistro = info[0]
ver = info[1]
print(ldistro)
print (ver)
#appid for discord app
appid = "none"
#number of packages
packages = "none"
#find out uptime for epoch time
uptime = exec_bash("cat /proc/stat | grep btime | awk '{print $2}'")
# predefine ids
cpuid = "none"
cpuappid = "none"
gpuid = "none"
termappid = "none"
desktopid = "none"
#distros set id and package number
def iUbuntu():
	global appid, packages
	appid='740434138036699178'
	packages = exec_bash("dpkg-query -f '.\n' -W | wc -l")

def iVoid():
        global appid, packages
        appid='740484961353597039'
def iOpenSuseLeap():
	global appid, packages
	appid='740156532137787433'
	packages = exec_bash("rpm -qa --last | wc -l")
def iOpenSuseTumble():
	global appid, packages
	appid='740156532137787433'
	packages = exec_bash("rpm -qa --last | wc -l")
def iCentos():
	global appid, packages
	appid='740483295388631071'
	packages = exec_bash("rpm -qa --last | wc -l")
def iArch():
	global appid, packages
	appid='740476198437650473'
	packages = exec_bash("pacman -Qq --color never | wc -l")
def iFedora():
	global appid, packages
	appid='740485660703719464'
	packages = exec_bash("rpm -qa --last | wc -l")
def iGentoo():
	global appid, packages
	appid='740484380652208140'
	packages = exec_bash("eix-installed -a | wc -l")
def iDebian():
	global appid, packages
	appid='740490017218232392'
	packages = exec_bash("dpkg-query -f '.\n' -W | wc -l")
def iManjaro():
	global appid, packages
	appid='740614258177605642'
	packages = exec_bash("pacman -Qq --color never | wc -l")
def iLinuxMint():
        global appid, packages
        appid='740633577481568317'
        packages = exec_bash("dpkg-query -f '.\n' -W | wc -l")
def iLMDE():
        global appid
        appid='741726946588622988'
def iPop():
	global appid, packages
	appid='740660055925587978'
	packages = exec_bash("dpkg-query -f '.\n' -W | wc -l")
def iEnde():
	global appid, packages
	appid='740809641545564170'
	packages = exec_bash("pacman -Qq --color never | wc -l")
#def desktops and defind id
def iKde():
	global desktopid, desktopver
	desktopid = "kde"
	#desktopver = exec_bash("plasmashell --version")
def iGnome():
	global desktopid, desktopver
	desktopid = "gnome"
	#desktopver = exec_bash("")
def iXfce():
	global desktopid, desktopver
	desktopid = "xfce"
	#desktopver = exec_bash("")
def Ii3():
	global desktopid, desktopver
	desktopid = "i3"
	#desktopver = exec_bash("")
def iCinnamon():
	global desktopid, desktopver
	desktopid = "cinnamon"
	#desktopver = exec_bash("")
def iBudgie():
	global desktopid, desktopver
	desktopid = "budgie"
	#desktopver = exec_bash("")
def iDeepin():
	global desktopid, desktopver
	desktopid = "deepin"
	#desktopver = exec_bash("")
def iDwm():
	global desktopid, desktopver
	desktopid = "dwm"
def iAwesome():
	global desktopid, desktopver
	desktopid = "awesome"
def iMate():
	global desktopid, desktopver
	desktopid = "mate"
def iUnity():
	#this is to check wether the user is actually using unity or using unity as an xdg value to fix issues with electron apps
	if wmid.lower() == "compiz":
		global desktopid
		desktopid = "unity"
	else:
		desktopid = wmid
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
# gpuids
def Nvidiagpu():
        global gpuid
        gpuid = "nvidia"
def Amdgpu():
        global gpuid
        gpuid = "amd"
def Intelgpu():
        global gpuid
        gpuid = "intel"
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
#pretty name, this will be shown when hovering over the big icon, it will show the version
prettyname = ldistro + ' ' + ver
print (prettyname)
#list of distros to comopre
amdcpus = {
    "ryzen 3": Ryzen3,
    "ryzen 5": Ryzen5,
    "ryzen 7": Ryzen7,
    "ryzen 9": Ryzen9,
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
}
distros = {
"ubuntu": iUbuntu, 
"opensuse-leap": iOpenSuseLeap,
"arch": iArch, 
"artix": iArch,
"fedora": iFedora,
"void": iVoid,
"gentoo": iGentoo,
"centos": iCentos,
"debian": iDebian,
"opensuse-tumbleweed": iOpenSuseTumble,
"manjaro": iManjaro,
"linuxmint": iLinuxMint,
"lmde": iLMDE,
"pop": iPop,
"endeavouros": iEnde
}
# window managers
windowmanagers = {
    "dwm": iDwm,
    "i3": Ii3,
    "awesome": iAwesome,
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
	"unity": iUnity
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
}
shells = {
    "fish": Fish,
    "zsh": Zsh,
    "bash": Bash,
}
try:
	distros[sysosid.lower()]()
except KeyError:
	print("Unsupported Distro, contact me on the GitHub page to resolve this.(keyerror)")
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

#package number
packtext = 'Packages: ' + packages
#if de in desktops:
print(cpuid)
