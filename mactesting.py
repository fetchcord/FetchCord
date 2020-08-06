import os
packages = os.popen("ls -l /Applications | wc -l").read()
appsp = "Applications: " + packages
ver = os.popen("sw_vers -productVersion").read()
uptime = os.popen("sysctl -n kern.boottime").read()
product = os.popen("sysctl -n hw.model").read()
kernel = os.popen("uname -r").read()
ruptime = uptime.split()
devicetype = "none"
macver = "none"
bigicon = "none"
uptime = ruptime[3]
print (uptime[:-1])
def iHsiera():
	global bigicon
	bigicon = "hsierria"
def iMojave():
	global bigicon
	bigicon = "mojave"
def iCatilina():
	global bigicon
	bigicon = "catilina"

versions ={
	"10.13": iHsiera,
	"10.14": iMojave,
	"10.15": iCatilina
}
def laporp():
	global devicetype
	if product[0:7] == "MacBook":
		devicetype = "laptop"
	else:
		devicetype = "desktop"
def findver():
	global bigicon
	try:
		versions[ver[0:5]]()
	except IndexError:
		bigicon = "bigslurp"
	except KeyError:
		print("Unsupported MacOS version")
findver()
laporp()