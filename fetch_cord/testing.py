# import shit as usual
import os
import sys
from fetch_cord.args import parse_args
from fetch_cord.bash import exec_bash
from fetch_cord.out import cpumodel, cpuvendor, gpuvendor, sysosid
if os.name != "nt":
    from fetch_cord.out import wmid, deid, termid, shellid, sysosid, hostline, termline
elif os.name == "nt":
    from fetch_cord.out import moboline

# appid for discord app
appid = "none"

# predefine ids
cpuappid = "none"
gpuid = "none"
termappid = "none"
desktopid = "none"
hostappid = "none"


def Unknown_distro():
    global appid
    appid = '742887089179197462'

def Unknown_de_wm():
    global desktopid
    desktopid = 'unknown'

def Unknown_cpu():
    global cpuid, cpuappid
    cpuappid = '742887089179197462'

def Unknown_gpu():
    global gpuid
    gpuid = 'unknown'

def Unknown_term():
    global termappid
    termappid = '742887089179197462'

def Unknown_shell():
    global shell
    shell = "unknown"

def Unknown_host():
    global hostappid, moboid
    hostappid = "742887089179197462"
    moboid = 'unknown'


# macOS hardwawre


def laporp():
    global devicetype
    if product[0:7] == "MacBook":
        devicetype = "laptop"
    else:
        devicetype = "desktop"

def macos():
    global product, devicetype, bigicon, ver
    if sysosid.lower() == "macos":
        devicetype = "none"
        bigicon = "none"
        ver = os.popen("sw_vers -productVersion").read()
        product = os.popen("sysctl -n hw.model").read()
        try:
            bigicon = versions[ver[0:5]]
        except IndexError:
            bigicon = "bigslurp"
        except KeyError:
            print("Unsupported MacOS version")
        laporp()

# this is staying
def iUnity():
    # this is to check wether the user is actually using unity
    # or using unity as an xdg value to fix issues with electron apps
    if wmid.lower() == "compiz":
        global desktopid
        desktopid = "unity"
    else:
        desktopid = wmid

amdcpus = {
    "ryzen 3": '741153175779803146',
    "ryzen 5": '741152732756312125',
    "ryzen 7": '740752899054895105',
    "ryzen 9": '741152930899427364',
    "ryzen threadripper": '742075019257184338',
}
intelcpus = {
    "intel i3": '741044208512532570',
    "intel i5": '741099939198926920',
    "intel i7": '741100300219187335',
    "intel i9": '741100622040006719',
    "intel pentium": '741203845706940467',
    "intel celeron": '742904581360713849',
    "pentium": '741203845706940467',
}
gpus = {
    "intel": "intel",
    "intel(r)": "intel",
    "nvidia": "nvidia",
    "amd": "amd",
    "radeon": "amd",
    "vmware": "vmware",
    "virtio": "virtio",
    # multi GPUs
    "nvidiaintel": "nvidia-intel",
    "nvidiaamd": "nvidia-amd",
    "amdintel": "amd-intel",
    "radeonintel": "amd-intel",
    "nvidiaamdintel": "nvidia-amd-intel",
}
distros = {
    "ubuntu": '740434138036699178',
    "opensuseleap": '740156532137787433',
    "arch": '740476198437650473',
    "arco": '745435867971321866',
    "artix": '741918141248045107',
    "fedora": '740485660703719464',
    "void": '740484961353597039',
    "gentoo/linux": '740484380652208140',
    "funtoo": '740484380652208140',
    "centos": '740483295388631071',
    "debian": '740490017218232392',
    "opensusetumbleweed": '742180413132505088',
    "manjaro": '740614258177605642',
    "linuxmint": '740633577481568317',
    "lmde": '741726946588622988',
    "pop!_os": '740660055925587978',
    "endeavouros": '740809641545564170',
    "windows10": '741949889465942099',
    "windows7": '741952383512346696',
    "windows8": '741952179488948324',
    "windows8.1": '741952065294827520',
    "nixos": '744644133494325329',
    "instantos": '744784599653285938',
    "freebsd": '745054697047457822',
    "funtoo": '740484380652208140',
}
versions = {
    "10.13": "hsierria",
    "10.14": "mojave",
    "10.15": "catalina",
}
# window managers
windowmanagers = {
    "dwm": "dwm",
    "i3": "i3",
    "awesome": "awesome",
    "enlightenment": "enlightenment",
    "bspwm": "bspwm",
    "xmonad": "xmonad",
    "sway": "sway",
}
# desktops
desktops = {
    "kde": "kde",
    "plasma": "kde",
    "xfce": "xfce",
    "budgie": "budgie",
    "gnome": "gnome",
    "deepin": "deepin",
    "cinnamon": "cinnamon",
    "mate": "mate",
    "unity": iUnity,
    "aero": "aero",
    "pantheon": "pantheon",
}
terminals = {
    "st": '741280043220861030',
    "kitty": '741285676250824725',
    "alacritty": '741291339945345045',
    "xterm": '741287143187546125',
    "konsole": '741286819676553258',
    "dolphin": '741286819676553258',
    "gnome-terminal": '741328861115056160',
    "cool-retro-term": '741731097498353794',
    "urxvt": '743246048968835092',
    "xfce4-terminal": '744332423072055296',
    "apple_terminal": '744950796298354689',
}


shells = {
    "fish": "fish",
    "zsh": "zsh",
    "bash": "bash",
}
hosts= {
    "inspiron": "743970870631858288",
    "latitude": "743970870631858288",
    "g3": "743970870631858288",
    "hp": "743971270395297852",
    "tuf": '744330890343219262',
    "asus": "743936082780880928",
    "asustek": "743936082780880928",
    "acer": '744326890512318544',
    "thinkpad": '744326223412461630',
    "lenovo": '744326223412461630',
}

args = parse_args()

hostlist = ['Acer', 'TUF', 'HP', 'ThinkPad', 'Inspiron', 'Lenovo', 'Latitude', 'G3', 'Asus', 'ASUSTeK']
hostid = ""
if os.name != "nt":
    if hostline != "":
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
    if moboline != "":
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


terminallist = ["st", "kitty", "alacritty", "xterm", "konsole", "gnome-terminal", "cool-retro-term", "urxvt", "xfce4-terminal", "terminator", "tmux"]
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
        Unknown_term()

    try:
        shell = shells[shellid.lower()]
    except KeyError:
        print("Unsupported Shell, contact us on guthub to resolve this.(Keyerror)")
        Unknown_shell()
    try:
        if sysosid.lower() != "macos":
            hostappid = hosts[hostid.lower()]
    except KeyError:
        print("Unknown Host, contact us on github to resolve this.(Keyerror)")
        Unknown_host()

    try:
        if deid != "N/A" and sysosid.lower() != "macos":
            desktopid = desktops[deid.lower()]
    except KeyError:
        print("Unsupported De contact us on github to resolve this.(Keyerror)")
        Unknown_de_wm()

    try:
        if deid == "N/A" and sysosid.lower() != "macos":
            desktopid = windowmanagers[wmid.lower()]
    except KeyError:
        print("Unsupported Wm contact us on github to resolve this.(Keyerror)")
        Unknown_de_wm()

    try:
        if sysosid.lower() != "macos":
          appid = distros[sysosid.lower()]
    except KeyError:
        print("Unsupported Distro, contact us on the GitHub page to resolve this.(keyerror)")
        Unknown_distro()

    try:
        if cpuvendor == "AMD":
            cpuappid = amdcpus[cpumodel.lower()]
        elif cpuvendor in ["Intel", "Pentium"]:
            cpuappid = intelcpus[cpumodel.lower()]
    except KeyError:
        print("unknown CPU, contact us on github to resolve this.(Keyerror)")
        Unknown_cpu()

    try:
        gpuid = gpus[gpuvendor.lower()]
    except KeyError:
        print("Unknown GPU, contact us on github to resolve this.(Keyerror)")
        Unknown_gpu()
if os.name == "nt":
    try:
        moboid = hosts[moboid.lower()]
    except KeyError:
        print("Unknown Host, contact us on github to resolve this problem.(Keyerror)")
        Unknown_host()

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
