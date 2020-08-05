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
def iUbuntu():
	global appid, packages
	appid='740434138036699178'
	packages = os.popen("dpkg-query -f '.\n' -W | wc -l").read()

def iVoid():
	global appid, packages
	appid='740156532137787433'
	packages = os.popen("xbps-query -l | wc -l").read()
def iOpenSuseLeap():
	global appid, packages
	appid='740156532137787433'
	packages = os.popen("rpm -qa --last | wc -l").read()

def iCentos():
	global appid, packages
	appid='740156532137787433'
	packages = os.popen("rpm -qa --last | wc -l").read()

def iArch():
	global appid, packages
	appid='740156532137787433'
	packages = os.popen("pacman -Qq --color never").read()

def iFedora():
	global appid, packages
	appid='740156532137787433'
	packages = os.popen("rpm -qa --last | wc -l").read()

def iGentoo():
	global appid, packages
	appid='740156532137787433'
	#packages = os.popen("rpm -qa --last | wc -l").read()
#pretty name, this will be shown when hovering over the big icon, it will show the version
prettyname = ldistro + ' ' + ver
print (prettyname)

distros = {
"ubuntu": iUbuntu, 
"opensuse-leap": iOpenSuseLeap,
"arch": iArch,
"fedora": iFedora,
"void": iVoid,
"gentoo": iGentoo,
"centos": iCentos,

}
try:
	distros[ldistro]()
except KeyError:
	print("Unsupported Distro, contact me on the GitHub page to resolve this.(keyerror)")
#package number
packtext = 'Packages: ' + packages
