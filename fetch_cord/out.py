from .bash import exec_bash, BashError
import subprocess
baseinfo = exec_bash("neofetch --stdout")
#make lists
cpu = "CPU:"
cpuline = []
gpu = "GPU"
gpuline = []
term = "Terminal:"
termline = []
termfont = "Terminal Font:"
termfontline = []
wm = "WM:"
wmline = []
de = "DE:"
deline = []
shell = "Shell:"
shell_line = []
kernel = "Kernel:"
kernelline = []
os = "OS:"
osline = []
packages = "Packages:"
packagesline = []
filepath = "out"
with open(filepath, 'w') as f:
    print(baseinfo, file=f)
with open(filepath, "rt") as f:
    for line in f:
        if line.find(cpu) != -1:
            cpuline.append(line.rstrip('\n'))
        if line.find(gpu) != -1:
            gpuline.append(line.rstrip('\n'))
        if line.find(term) != -1:
            termline.append(line.rstrip('\n'))
        if line.find(termfont) != -1:
            termfontline.append(line.rstrip('\n'))
        if line.find(de) != -1:
            deline.append(line.rstrip('\n'))
        if line.find(wm) != -1:
            wmline.append(line.rstrip('\n'))
        if line.find(shell) != -1:
            shell_line.append(line.rstrip('\n'))
        if line.find(packages) != -1:
            packagesline.append(line.rstrip('\n'))
        if line.find(kernel) != -1:
            kernelline.append(line.rstrip('\n'))
        if line.find(os) != -1:
            osline.append(line.rstrip('\n'))
try:
    check_provider = exec_bash("xrandr --listproviders | grep -o \"NVIDIA.*\"")
except BashError:
    pass
    check_provider = ""
if check_provider == "":
    try:
        # amd GPUs
        gpuline = "GPU: " + exec_bash("glxinfo | grep \"OpenGL renderer string:\" | sed 's/^.*: //;s/(.*//;s/Mesa //'")
        gpuvendor = gpuline.split()[1]
        if gpuvendor == "Intel":
            gpuline = "GPU: " + exec_bash("glxinfo | grep \"OpenGL renderer string:\" | sed 's/^.*: //;s/Mesa //'")
        gpuinfo = gpuline
        gpuid = gpuline
        print(gpuid)
        print(gpuline)
    except BashError as e:
        print("ERROR: Could not run glxinfo [%s]" % str(e))
        sys.exit(1)
else:
    try:
        # Optimus Configuration
        gpuvendor = gpuline[1].split()[1]
        gpuinfo = gpuline[1]
    except IndexError:
        pass
        gpuvendor = gpuline[0].split()[1]
        gpuinfo = gpuline[0]
    print(gpuinfo)
    print(gpuvendor)
    print(gpuline)
cpuvendor = cpuline[0].split()[1]
if cpuvendor == "Intel":
    cpumodel = cpuline[0].replace('-', ' ').split()[1] + ' ' + cpuline[0].replace('-', ' ').split()[2]#] + ' ' + cpuline[0].split()[3]
elif cpuvendor == "AMD":
    cpumodel = cpuline[0].split()[2] + ' ' + cpuline[0].split()[3]
cpuinfo = cpuline[0].join(cpuline)[5:]
wmid = wmline[0].split()[1]
termid = termline[0].split()[1]
shellid = shell_line[0].split()[1]
kernelid = kernelline[0].split()[1]
osid = osline[0].split()[1]
if not termfontline:
    termfontline = []
    termfontline.append("Terminal font: N/A")
    print(termfontline[0])
if deline:
    deid = deline[0].split()[1]
    print(deid)
else:
    deid = "none"
print(wmid)
print(termid)
print(cpuvendor)
print(cpumodel)
print(cpuinfo)
print(gpuinfo)
print(gpuvendor)
print(packagesline[0])
print(cpuline[0])
print(termline[0])
print(osid)
print(wmline[0])
