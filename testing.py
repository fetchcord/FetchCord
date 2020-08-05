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

def iCentos():
	global appid, packages
	appid='740483295388631071'
	packages = os.popen("rpm -qa --last | wc -l").read()

def iArch():
	global appid, packages
	appid='740476198437650473'
	packages = os.popen("pacman -Qq --color never").read()

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
"debian": iDebian
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
	"dwm": iDwm
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