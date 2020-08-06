import distro
import os
info = distro.linux_distribution(full_distribution_name=False)
ldistro= info[0]
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
desplit = getdesk.split()
de = desplit[0]
wm = desplit[1]
desktopid = "none"
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

#pretty name, this will be shown when hovering over the big icon, it will show the version
prettyname = ldistro + ' ' + ver
print (prettyname)
#list of distros to comopre
distros = {
"ubuntu": iUbuntu, 
"opensuse-leap": iOpenSuseLeap,
"arch": iArch,
"fedora": iFedora,
"void": iVoid,
"gentoo": iGentoo,
"centos": iCentos,
"debian": iDebian,
"opensuse-tumbleweed": iOpenSuseTumble,
"manjaro": iManjaro,
"linuxmint": iLinuxMint,
"pop": iPop,
"artix": iArch,
"endeavouros": iEnde
}
#desktops
desktops = {
	"kde": iKde,
	"xfce": iXfce,
	"budgie": iBudgie,
	"gnome": iGnome,
	"deepin": iDeepin,
	"cinnamon": iCinnamon,
	"i3": Ii3,
	"dwm": iDwm,
	"awesome": iAwesome,
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
	print("Unsupported De/Wm contact me on github to resolve this.(Keyerror)")


#package number
packtext = 'Packages: ' + packages
print (de.lower())