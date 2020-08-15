<h1 align="center">FetchCord</h1>
</p>
<p align="center">
    <a href="https://img.shields.io/badge/Compatible-MacOS%2FWindows%2FLinux-brightgreen?style=for-the-badge&logo=discord">
       <img src="https://img.shields.io/badge/Compatible-MacOS%2FLinux-brightgreen?style=for-the-badge&logo=linux&logoColor=white">
    </a>
  <a href="https://www.python.org/downloads/">
       <img src="https://img.shields.io/pypi/pyversions/django?color=dark%20green&logo=python&logoColor=white&style=for-the-badge">
    </a>
   <a href="https://discord.gg/P4h9kdV">
       <img src="https://img.shields.io/discord/742068289278312549?label=Discord&logo=discord&logoColor=white&style=for-the-badge">
    </a>
    <a href="https://img.shields.io/badge/Compatible-MacOS%2FWindows%2FLinux-brightgreen?style=for-the-badge&logo=discord">
       <img src="https://cdn.discordapp.com/attachments/695182849476657223/742064452421288077/FetchDis.png"
    </a>
  
  </a>
</p>

# Table of content
- [**Features**](#features)
- [**To-Do**](#to-do)
+ **Installing**
    - [Install on (gnu/)linux](#installing-on-gnulinux)
    - [Install on MacOS](#installing-on-macos)
 + **Running**
    - [Running on (gnu/)linux](#run)
       - [Arguments](#arguments)
    - [Running on MacOS](#run1)

- [**Examples**](#examples)

### Features

- [x] Distribution detection
 
- [x] Distribution Version

- [x] Package detection

- [x] Kernel Detection

- [x] Uptime

- [x] Detecting Window Manager/Desktop Environment

- [x] Detecting GPU/CPU and display it in a cycle (thanks to Hyper-KVM)
- [x] Flatpak support

### To-Do

- [ ] Add more distributions (If your distro is not supported open an issue)

- [ ] Detect Window Manager/Desktop Environment version

- [ ] Add Snap support

- [ ] Add support for desktop icon use

- [ ] More CPUs, ex. Pentium, Older AMD CPUs

- [ ] More GPUs?

- [ ] Add Windows support. [WIP]


## Installing on (GNU/)Linux

On Arch Linux install this package for the git version: [fetchcord-git](https://aur.archlinux.org/packages/fetchcord-git/)

On other distros and the non git version: `pip3 install fetchcord`

NOTE: you need neofetch to be also installed for this to work.

If you want to remove FetchCord you can run `pip3 uninstall fetchcord`

You can copy the discord script to somewhere in PATH to have fetchcord run upon opening discord, making sure the discord script is executable. `sudo chmod +x /path/to/discord/script`

### Run

Once installed, simply run `fetchcord`.

If that does not work,add /home/$USER/.local/bin/ to your path, or just run `python3 -m fetchcord`.

#### Arguments
--distro, shows only distro and kernel version and package count or with other args combined.

--hardware, shows only CPU and GPU info or with other args combined.

--shell, shows only terminal and shell info or with other args combined.

--host, shows only host info or with other args combined.

--time, -t, set custom duration for cycles in seconds.

--terminal, set custom terminal (useful if using a script or dmenu).

--termfont, set custom terminal font (useful if neofetch can't get it).

-h or --help, shows this information above.

## Installing on MacOS

To install FetchCord, run `pip3 install FetchCord`

NOTE: you need neofetch to be also installed for this to work.

### Run 

simply run `fetchcord`

## Examples

![Arch with awesome](Examples/arch_example.png) ![Debian with Cinnamon](Examples/debian_example.png) ![Fedora with xfce](Examples/fedora_example.png)

![manjaro with i3](Examples/manjaro%20example.png) ![mint with mate](Examples/mint_example.png) ![popos with kde](Examples/pop_example.png)

![void with dwm](Examples/void_example.png) ![endeabour with deepinde](Examples/end_example.png) ![centos with unity](Examples/centos_example.png)

![ubuntu with budgie](Examples/ubuntu_example.png) ![macos with a macbook](Examples/mac_example.png) ![OpenSUSE with gnome](Examples/suse_example.png)

![amd with nvidia](Examples/amd_example.png)


