# FetchCord
![Compatible](https://img.shields.io/badge/Compatible-MacOS%2FWindows%2FLinux-brightgreen)
![version](https://img.shields.io/badge/Python-version%3A%203.8-red)

_Fetchcord grabs information about your distribution and displays it as Discord Rich Presence._

### Examples
![ubuntu with budgie](Examples/ubuntu_example.png) ![macos with a macbook](Examples/mac_example.png) ![OpenSUSE with gnome](Examples/suse_example.png)

![amd with nvidia](Examples/amd_example.png)

[Find us on Discord](https://discord.gg/P4h9kdV) 

***
+ What works
  - [✓] Distribution detection

  - [✓] Distribution Version

  - [✓] Package detection

  - [✓] Kernel Detection

  - [✓] Uptime

  - [✓] Detecting Window Manager/Desktop Environment

  - [✓] Detecting GPU/CPU and display it in a cycle (thanks to Hyper-KVM)

***
+ To-Do
  - [✗] Add more distributions (If your distro is not supported open an issue)

  - [✗] Detect Window Manager/Desktop Environment version

  - [✗] Add Flatpak/Snap support

  - [✗] Add support for desktop icon use

  - [✗] More CPUs, ex. Pentium, Older AMD CPUs

  - [✗] More GPUs?

***

### Running on (GNU/)Linux
> `#` the command should be ran as `sudo`

> `$` the command should be ran as user

#####Install
_From download/cloned directory_


```sh
# ./install.sh
```


To run the script simply run `fetchcord`, python 3.8 should have the `distro` module but if you get an error install it via pip,

```sh
$ pip3 install distro
```

python3.8 needs the `distro` module. If you get an error, install it via pip: `pip3 install distro`

## Running on MacOS
#####Install
_From download/cloned directory_

```sh
# ./macinstall.sh
```


#####Run 

```sh
$ python3 -u -m fetch_cord.macos-rpc.py
```

## Other Examples

![Arch with awesome](Examples/arch_example.png) ![Debian with Cinnamon](Examples/debian_example.png) ![Fedora with xfce](Examples/fedora_example.png)

![manjaro with i3](Examples/manjaro%20example.png) ![mint with mate](Examples/mint_example.png) ![popos with kde](Examples/pop_example.png)

![void with dwm](Examples/void_example.png) ![endeabour with deepinde](Examples/end_example.png) ![centos with unity](Examples/centos_example.png)

