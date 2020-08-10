# FetchCord

Fetchcord grabs information about your distribution and displays it as Discord Rich Presence.

## Examples
![ubuntu with budgie](Examples/ubuntu_example.png) ![macos with a macbook](Examples/mac_example.png) ![OpenSUSE with gnome](Examples/suse_example.png)

![amd with nvidia](Examples/amd_example.png)

## What works

- [x] Distribution detection

- [x] Distribution Version

- [x] Package detection

- [x] Kernel Detection

- [x] Uptime

- [x] Detecting Window Manager/Desktop Environment

- [x] Detecting GPU/CPU and display it in a cycle (thanks to Hyper-KVM)

- [x] Add Flatpak support

## To-Do
- [ ] Add more distributions (If your distro is not supported open an issue)

- [ ] Detect Window Manager/Desktop Environment version

- [ ] Add Snap support

- [ ] Add support for desktop icon use

- [ ] More CPUs, ex. Pentium, Older AMD CPUs

- [ ] More GPUs?


## Arguments

--distro, shows only distro and kernel version and package count.

--hardware, shows only CPU and GPU info.

--shell, shows only terminal and shell info.

--time, -t, set custom duration for cycles in seconds.
 
 -h or --help, shows this information above.

## Running on (GNU/)Linux

To install the script, run `sudo ./install.sh`.

To run the script simply run `fetchcord`, python 3.8 should have the `distro` module but if you get an error install it via pip, `pip3 install distro`

NOTE: This script requires neofetch to be installed.

python3.8 needs the `distro` module. If you get an error, install it via pip: `pip3 install distro`

## Running on MacOS
To install the script, run `sudo ./install.sh`.

Run `python3 run-rpc.py`.

## Other Examples

![Arch with awesome](Examples/arch_example.png) ![Debian with Cinnamon](Examples/debian_example.png) ![Fedora with xfce](Examples/fedora_example.png)

![manjaro with i3](Examples/manjaro%20example.png) ![mint with mate](Examples/mint_example.png) ![popos with kde](Examples/pop_example.png)

![void with dwm](Examples/void_example.png) ![endeabour with deepinde](Examples/end_example.png) ![centos with unity](Examples/centos_example.png)

