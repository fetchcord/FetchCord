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
getdesk = os.popen("bash getdewm.sh").read()
getcpu = os.popen("cat /proc/cpuinfo | awk '/^vendor/{print $3}' | uniq").read()
cpusplit = getcpu.splitlines()

if cpusplit[0] == "AuthenticAMD":
    cpu = "amd"
else:
    cpu = "intel"

desplit = getdesk.split()
for i in range(len(desplit)):
    de = desplit[i]
    wm = desplit[i]
desktopid = "none"
cpuid = "none"
#desktopver = "none"
#distros set id and package number
def iUbuntu():
	global appid, packages
	appid='740434138036699178'
	packages = os.popen("dpkg-query -f '.\n' -W | wc -l").read()

def iVoid():
	global appid, packages
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
	#packages = os.popen("rpm -qa --last | wc -l").read()
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
# cpuids
def Amd():
        global cpuid
        cpuid = "amd"
def Intel():
        global cpuid
        cpuid = "intel"
#pretty name, this will be shown when hovering over the big icon, it will show the version
prettyname = ldistro + ' ' + ver
print (prettyname)
#list of distros to comopre
cpus = {
"amd": Amd,
"intel": Intel,
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
"pop": iPop,
}
# window managers
windowmanagers = {
    "dwm": iDwm,
    "i3": Ii3,
}
#desktops
desktops = {
	"kde": iKde,
	"xfce": iXfce,
	"budgie": iBudgie,
	"gnome": iGnome,
	"deepin": iDeepin,
	"cinnamon": iCinnamon,
}
try:
	distros[ldistro]()
except KeyError:
	print("Unsupported Distro, contact me on the GitHub page to resolve this.(keyerror)")
try: 
    if de in desktops:
        desktops[de.lower()]()
    else:
        pass
except KeyError:
	print("Unsupported De contact me on github to resolve this.(Keyerror)")
pass
try:
        windowmanagers[wm.lower()]()
except KeyError:
        print("Unsupported Wm contact me on github to resolve this.(Keyerror)")
try:
        cpus[cpu.lower()]()
except KeyError:
        print("ERROR: unknown CPU")

#package number
packtext = 'Packages: ' + packages
if de in desktops:
    print (de.lower())
print(wm.lower())
print(cpuid)
