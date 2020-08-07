import distro
import os
info = distro.linux_distribution(full_distribution_name=False)
ldistro = info[0]
ver = info[1]
print(ldistro)
print (ver)
#appid for discord app
appid = "none"
#find kernel
info = os.popen("uname -r").read()
#number of packages
packages = "none"
#text for kernel info
text = 'Kernel: ' + info
#find out uptime for epoch time
uptime = os.popen("cat /proc/stat | grep btime | awk '{print $2}'").read()
#set appid and packages for each distro 
getde = os.popen("/usr/local/bin/getde").read()
getwm = os.popen("/usr/local/bin/getwm").read().split()
# get cpu info
getcpufam = os.popen("lscpu | awk '/^CPU family/{print $3}'").read().split()
cpuvendor = os.popen("lscpu | awk '/^Vendor ID:/{print $3}'").read().split()
getcpumodel = os.popen("cat /proc/cpuinfo | awk '/^model name/{print $4,$5,$6,$7}' | uniq").read().splitlines()
cpu = getcpufam[0]
cpumodel = "CPU: " + getcpumodel[0]
cpuinfo = getcpumodel[0]
cpufam = getcpufam
# set cpuid
cpuid = "none"
cpuappid = "none"
# get gpu
check_provider = os.popen("xrandr --listproviders | egrep -io \"name:.*NVIDIA-G0.*\" | sed 's/name://'").read()
if check_provider == "NVIDIA-G0\n":
    gpu = os.popen(" lspci | egrep \"VGA.*\" | grep -o \"\[.*.*\].*\" | sed 's/^\[//;s/]//;s/(rev ..)//'").read()
    gpuvendor = os.popen("__NV_PRIME_RENDER_OFFLOAD=1 __GLX_VENDOR_LIBRARY_NAME=nvidia glxinfo | grep \"OpenGL vendor string:\" | awk '{print $4}'").read().split()
else:
    gpu = os.popen("glxinfo | grep \"OpenGL renderer string:\" | sed 's/OpenGL renderer string: //;s/Mesa //'").read()
    gpuvendor = os.popen("glxinfo | grep \"OpenGL vendor string:\" | awk '{print $4}'").read().split()
# get gpu info
getgpuout = gpu.splitlines()
gpuout = "GPU: " + getgpuout[0]
gpuinfo = gpu
print(check_provider)
print(gpuout)
de = getde
wm = getwm[0]
desktopid = "none"
#distros set id and package number
def iUbuntu():
	global appid, packages
	appid='740434138036699178'
	packages = os.popen("dpkg-query -f '.\n' -W | wc -l").read()

def iVoid():
        global appid, packages, appid2
        appid='740484961353597039'
        packages = os.popen("xbps-query -l | wc -l").read()
def iOpenSuseLeap():
	global appid, packages
	appid='740156532137787433'
	packages = os.popen("rpm -qa --last | wc -l").read()
def iOpenSuseTumble():
	global appid, packages
	appid='740156532137787433'
	packages = os.popen("rpm -qa --last | wc -l").read()
def iCentos():
	global appid, packages
	appid='740483295388631071'
	packages = os.popen("rpm -qa --last | wc -l").read()
def iArch():
	global appid, packages
	appid='740476198437650473'
	packages = os.popen("pacman -Qq --color never | wc -l").read()
def iFedora():
	global appid, packages
	appid='740485660703719464'
	packages = os.popen("rpm -qa --last | wc -l").read()
def iGentoo():
	global appid, packages
	appid='740484380652208140'
	packages = os.popen("eix-installed -a | wc -l").read()
def iDebian():
	global appid, packages
	appid='740490017218232392'
	packages = os.popen("dpkg-query -f '.\n' -W | wc -l").read()
def iManjaro():
	global appid, packages
	appid='740614258177605642'
	packages = os.popen("pacman -Qq --color never | wc -l").read()
def iLinuxMint():
        global appid, packages
        appid='740633577481568317'
        packages = os.popen("dpkg-query -f '.\n' -W | wc -l").read()
def iPop():
	global appid, packages
	appid='740660055925587978'
	packages = os.popen("dpkg-query -f '.\n' -W | wc -l").read()
def iEnde():
	global appid, packages
	appid='740809641545564170'
	packages = os.popen("pacman -Qq --color never | wc -l").read()
#def desktops and defind id
def iKde():
	global desktopid, desktopver
	desktopid = "kde"
	#desktopver = os.popen("plasmashell --version").read()
def iGnome():
	global desktopid, desktopver
	desktopid = "gnome"
	#desktopver = os.popen("").read()
def iXfce():
	global desktopid, desktopver
	desktopid = "xfce"
	#desktopver = os.popen("").read()
def Ii3():
	global desktopid, desktopver
	desktopid = "i3"
	#desktopver = os.popen("").read()
def iCinnamon():
	global desktopid, desktopver
	desktopid = "cinnamon"
	#desktopver = os.popen("").read()
def iBudgie():
	global desktopid, desktopver
	desktopid = "budgie"
	#desktopver = os.popen("").read()
def iDeepin():
	global desktopid, desktopver
	desktopid = "deepin"
	#desktopver = os.popen("").read()
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
	if wm.lower() == "compiz":
		global desktopid
		desktopid = "unity"
	else:
		desktopid = wm
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
def Intelcore4():
        global cpuid, cpuappid
        cpuid = "Intel Core(R) 4th Gen Series"
        cpuappid='741044208512532570'
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
#pretty name, this will be shown when hovering over the big icon, it will show the version
prettyname = ldistro + ' ' + ver
print (prettyname)
#list of distros to comopre
amdcpus = {
    "23": Ryzen,
    "22": Amdcpu,
}
intelcpus = {
    "6": Intelcore4,
}
gpus = {
    "intel": Intelgpu,
    "nvidia": Nvidiagpu,
    "x.org": Amdgpu,
}
print(cpu)
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
	"xfce": iXfce,
	"budgie": iBudgie,
	"gnome": iGnome,
	"deepin": iDeepin,
	"cinnamon": iCinnamon,
	"mate": iMate,
	"unity": iUnity
}
try:
	distros[ldistro]()
except KeyError:
	print("Unsupported Distro, contact me on the GitHub page to resolve this.(keyerror)")
try: 
        desktops[de.lower()]()
except KeyError:
	print("Unsupported De contact me on github to resolve this.(Keyerror)")
pass
try:
        windowmanagers[wm.lower()]()
except KeyError:
        print("Unsupported Wm contact me on github to resolve this.(Keyerror)")
try:
        if cpuvendor[0] == "AuthenticAMD":
            amdcpus[cpu.lower()]()
        else:
            intelcpus[cpu.lower()]()
except KeyError:
        print("unknown CPU, contact me on github to resolve this.(Keyerror)")

try:
        gpus[gpuvendor[0].lower()]()
except KeyError:
        print("Unknown GPU, contact me on github to resolve this.(Keyerror)")

#package number
packtext = 'Packages: ' + packages
#if de in desktops:
print (de.lower())
print(wm.lower())
print(cpuid)
