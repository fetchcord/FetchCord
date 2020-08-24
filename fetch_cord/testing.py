# import shit as usual
import os, sys, json
from fetch_cord.args import parse_args
from fetch_cord.bash import exec_bash
from fetch_cord.out import cpumodel, cpuvendor, gpuvendor, sysosid
if os.name != "nt":
    from fetch_cord.out import wmid, deid, termid, shellid, sysosid, hostline, termline
elif os.name == "nt":
    from fetch_cord.out import moboline

# macOS hardwawre

if os.name != "nt":
    def laporp(product):
        if product[0:7] == "MacBook":
            devicetype = "laptop"
        else:
            devicetype = "desktop"
        return devicetype

    def macos():
        devicetype = "none"
        ver = os.popen("sw_vers -productVersion").read()
        product = os.popen("sysctl -n hw.model").read()
        bigicon = "none"
        try:
            bigicon = versions[ver[0:5]]
        except IndexError:
            bigicon = "bigslurp"
        except KeyError:
            print("Unsupported MacOS version")
        laporp(product)
        return product, devicetype, bigicon, ver
    # this is staying
    def iUnity():
        # this is to check wether the user is actually using unity
        # or using unity as an xdg value to fix issues with electron apps
        if wmid.lower() == "compiz":
            desktopid = "unity"
        else:
            desktopid = wmid
        return desktopid

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources
import fetch_cord.ressources as ressources
with pkg_resources.open_text(ressources, 'infos.json') as f:
    infos = json.load(f)

amdcpus = infos["amdcpus"]
intelcpus = infos["intelcpus"]
gpus = infos["gpus"]
distros = infos["distros"]
versions = infos["versions"]
windowmanagers = infos["windowmanagers"]
desktops = infos["desktops"]
terminals = infos["terminals"]
shells = infos["shells"]
hosts= infos["hosts"]
motherboards= infos["motherboards"]
hostlist = infos["hostlist"]
terminallist = infos["terminallist"]

# desktops
if os.name != "nt":
    desktops["unity"] = iUnity()

args = parse_args()

hostid = ""
if os.name != "nt":
    if hostline:
        hostsplit = hostline[0].split()
        hostid = []
        for line in range(len(hostsplit)):
            if hostsplit[line] in hostlist:
                hostid.append(hostsplit[line].rstrip('\n'))
        try:
            hostid = hostid[0]
        except IndexError:
            hostid = ""
            pass

moboid = ""
if os.name == "nt":
    if moboline:
        mobosplit = moboline[0].split()
        moboid = []
        for line in range(len(mobosplit)):
            if mobosplit[line] in hostlist:
                moboid.append(mobosplit[line].rstrip('\n'))
        try:
            moboid = moboid[0]
        except IndexError:
            moboid = ""
            pass

if args.terminal:
    if args.terminal in terminallist:
        termid = args.terminal
        termline[0] = "Terminal: %s" % args.terminal
    else:
        print("\nInvalid terminal, only %s are supported.\n"
              "Please make a github issue if you would like to have your terminal added.\n"
              "https://github.com/MrPotatoBobx/FetchCord" % terminallist)
        sys.exit(1)


    if args.debug:
        print("hostsplit: %s" % hostsplit)
        print("hostid: %s" % hostid)

# bunch of try except blocks to catch keyerrors and tell the enduser that thier distro/others arent supported
if os.name != "nt":
    try:
        termappid = terminals[termid.lower()]
    except KeyError:
        print("Unsupported Terminal. contact us on github to resolve this.(Keyerror)")
        termappid = '745691250186911796'


    try:
        shell = [s for s in shells if shellid in s]
    except KeyError:
        print("Unsupported Shell, contact us on guthub to resolve this.(Keyerror)")
        shell = "unknown"

    try:
        if sysosid.lower() != "macos":
            hostappid = hosts[hostid.lower()]
    except KeyError:
        print("Unknown Host, contact us on github to resolve this.(Keyerror)")
        hostappid = "742887089179197462"

    try:
        if deid != "N/A" and sysosid.lower() != "macos":
            desktopid = desktops[deid.lower()]
    except KeyError:
        print("Unsupported De contact us on github to resolve this.(Keyerror)")
        desktopid = 'unknown'

    try:
        if deid == "N/A" and sysosid.lower() != "macos":
            desktopid = windowmanagers[wmid.lower()]
    except KeyError:
        print("Unsupported Wm contact us on github to resolve this.(Keyerror)")
        desktopid = 'unknown'

try:
    appid = distros[sysosid.lower()]
except KeyError:
    print("Unsupported Distro, contact us on the GitHub page to resolve this.(keyerror)")
    appid = '742993278143692821'

try:
    if cpuvendor == "AMD":
        cpuappid = amdcpus[cpumodel.lower()]
    elif cpuvendor in ["Intel", "Pentium"]:
        cpuappid = intelcpus[cpumodel.lower()]
    else:
        cpuappid = '742887089179197462'
except KeyError:
    print("unknown CPU, contact us on github to resolve this.(Keyerror)")
    cpuappid = '742887089179197462'

try:
    gpuid = gpus[gpuvendor.lower()]
except KeyError:
    print("Unknown GPU, contact us on github to resolve this.(Keyerror)")
    gpuid = 'unknown'

if os.name == "nt":
    try:
        moboid = motherboards[moboid.lower()]
    except KeyError:
        print("Unknown Host, contact us on github to resolve this problem.(Keyerror)")
        moboid = 'unknown'

elif sysosid.lower() == "macos":
    macos()


if args.debug:
    print("\n----testing.py----")
    if os.name != "nt":
        print("----DE/WM----\n")
        print("deid: %s" % deid)
        print("wmid: %s" % wmid)
        print("\n----TERMINAL/SHELL----\n")
        print("termid: %s" % termid)
        print("shellid: %s" % shellid)
        print("\n----HOST INFO----\n")
        print("hostid: %s" % hostid)
    elif os.name == "nt":
        print("moboid: %s" % moboid)
        print("moboline: %s" % moboline)
    print("\n----GPU INFO----\n")
    print("gpuvendor: %s" % gpuvendor)
    print("\n----CPU INFO----\n")
    print("cpumodel: %s\n" % cpumodel)
