# FetchCord

Fetchcord grabs information about your Distro and displays it as Discord Rich Presence

## Examples
![ubuntu with budgie](Examples/ubuntu_example.png) ![macos with a macbook](Examples/mac_example.png) ![OpenSUSE with gnome](Examples/suse_example.png) ![AMD Ryzen CPU/NVIDIA GPU](Examples/ryzen_example.png)
## What works

- [x] Distro detection

- [x] Package detection

- [x] Kernel Detection

- [x] Uptime

- [x] Distro version
- [x] Detect wm/de

- [x] Intel Core series CPU detection

- [x] AMD Ryzen series CPU detection

## To-Do(What doesn't work)

- [ ] Add more distros

- [ ] Detect wm/de version

- [ ] Add support for desktop icon use

- [ ] More CPUs, ex. Pentium, Older AMD CPUs

- [ ] More GPUs?


## Running on linux

To install the script, run `sudo ./install.sh` 

To run the script simply run `fetchcord` or start /usr/local/bin/discord, python 3.8 should have the `distro` module but if you get an error install it via pip, `pip3 install distro`

## If your distro or de/wm isn't supported, make an issue
## Snap and Flatpak versions of Discord will not work

## running on macos
To install the script, run `sudo ./macinstall.sh`

run `python3 -u -m macos-rpc.py` and it will work!

##  Other Examples

![Arch with awesome](Examples/arch_example.png) ![Debian with Cinnamon](Examples/debian_example.png) ![Fedora with xfce](Examples/fedora_example.png)

![manjaro with i3](Examples/manjaro%20example.png) ![mint with mate](Examples/mint_example.png) ![popos with kde](Examples/pop_example.png)

![void with dwm](Examples/void_example.png) ![endeabour with deepinde](Examples/end_example.png) ![centos with unity](Examples/centos_example.png)

