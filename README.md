<h1 align="center">FetchCord</h1>
</p>
<p align="center">
    <a href="https://img.shields.io/badge/Compatible-MacOS%2FWindows%2FLinux-brightgreen?style=for-the-badge&logo=discord">
       <img alt="Compatible OSes" src="https://img.shields.io/badge/Compatible-MacOS%2FLinux%2FWindows%2F-brightgreen?style=for-the-badge&logo=checkmarx&logoColor=white">
    </a>
  <a href="https://www.python.org/downloads/">
       <img alt="Python Versions" src="https://img.shields.io/pypi/pyversions/django?color=dark%20green&logo=python&logoColor=white&style=for-the-badge">
    </a>
   <a href="https://discord.gg/P4h9kdV">
       <img alt="Discord Server" src="https://img.shields.io/discord/742068289278312549?label=Discord&logo=discord&logoColor=white&style=for-the-badge">
    </a>
    <a href="https://img.shields.io/badge/Compatible-MacOS%2FWindows%2FLinux-brightgreen?style=for-the-badge&logo=discord">
       <img alt="Header Image" src="https://cdn.discordapp.com/attachments/695182849476657223/742064452421288077/FetchDis.png"
    </a>
  
  </a>
</p>

# Table of content
- [**Features**](#features)
- [**To-Do**](#to-do)
+ **Installing**
    - [Install on (gnu/)linux](#installing-on-gnulinux)
    - [Install on MacOS](#installing-on-macos)
    - [Install on Windows](#installing-on-windows)
 + **Running**
    - [Running on (gnu/)linux](#run)
    - [Running on MacOS](#run-1)
    - [Running on Windows](#run-2)
- [**Configuration**](#Configuration)
- [**Arguments**](#arguments)
- [**Website**](#website)

+ [**Examples**](#examples)

### Features

- [x] Distribution detection
 
- [x] Distribution Version

- [x] Package detection

- [x] Kernel Detection

- [x] Uptime

- [x] Detecting Window Manager/Desktop Environment

- [x] Detecting GPU/CPU and display it in a cycle (thanks to Hyper-KVM)

- [x] Flatpak support

- [x] Add Snap support

- [x] Add Windows support.

- [x] Detect Window Manager/Desktop Environment version

- [x] Periodic polling of info such as package count, RAM usage, etc.


### To-Do

- [ ] Add more distributions (If your distro is not supported open an issue)

- [ ] Add support for desktop icon use

- [ ] More CPUs, ex. Pentium, Older AMD CPUs

- [ ] More GPUs?


## Installing on (GNU/)Linux
NOTE: you need neofetch to be also installed for this to work.
#### Via AUR
On Arch Linux for the git testing version (the less stable version): [fetchcord-testing](https://aur.archlinux.org/packages/fetchcord-testing/)

And the git version (synced with master): [fetchcord](https://aur.archlinux.org/packages/fetchcord/)

Historically the stabler release was the one from [pip](#via-pip) but now master will have only the stable releases.
#### Via Snap
On systems with snap installed, you can run `sudo snap install fetchcord --classic` to install fetchcord.

Note that like the AUR version, this version is directly from master, for the stable release use [pip](#via-pip) <!-- remove this if you're not automatically deploying it -->
#### Via pip
To Install fetchcord via pip you can run `pip3 install fetchcord`

If you want to remove FetchCord you can run `pip3 uninstall fetchcord`

### Run

Once installed, simply run `fetchcord`. The program is also daemonizable meaning you can start it on boot using any method you prefer.

If you get `fetchcord: command not found`,add `export PATH="$HOME/.local/bin:$PATH"` to your bashrc, or just run `python3 -m fetchcord`.

Optionally for systemd users there is a user-side `fetchcord.service` in this repo that can be installed to `~/.local/share/systemd/user/`, started and enabled on boot using `systemctl --user enable --now fetchcord`.

## Installing on MacOS

To install FetchCord, run `pip3 install FetchCord`

NOTE: you need neofetch to be also installed for this to work. To do this, use `brew install neofetch`.

### Run 

simply run `fetchcord`

## Installing on Windows

To install fetchcord on Windows run `python -m pip install fetchcord neofetch-win`. Alternatively, you can use the neofetch package from scoop as well (show more info at the expense of possible GPU detection, for now).

### Run
To run Fetchcord run `fetchcord`

### Configuration

On Linux you can use the neofetch config file to:

Show disk usage

Battery level

CPU temp

Current CPU speed

Font

Theme

And more

default config path should be `~/.config/neofetch/config.conf`

## Arguments
`--nodistro`, Don't show distro info.

`--nohardware`, Don't show hardware info.

`--noshell`, Don't show shell/terminal info.

`--nohost`, Don't show host info.

`--noconfig`, Disable neofetch custom config. Enable if you have an incompatible custom configuration.

`--time TIME` or `-t TIME`, Set custom time in seconds for cycles. Default is 30 seconds seconds.

`--terminal TERMINAL`, Set custom Terminal (useful if using something like dmenu, or launching from a script).

`--termfont TERMFONT`, Set custom terminal font (useful if neofetch can't get it).

`--install`, Install fetchcord as a systemd service (user) and enable it.

`--uninstall`, Uninstall fetchcord as a systemd service (user).

`--enable`, Enable fetchcord systemd service (user).

`--disable`, Disable fetchcord systemd service (user).

`--start`, Start fetchcord systemd service (user).

`--stop`, Stop fetchcord systemd service (user).

`--status`, Get fetchcord systemd service status (user).

`--update`, Update database of distros, hardware, etc.

`--testing`, Get files from testing branch instead of master.

`--debug` or `-d`, Enable debugging.

`--pause-cycle`, Extra cycle that pauses for 30 seconds or custom time using --time argument.

`--memtype TYPE` or `-m TYPE`, Show Memory in GiB or MiB. Valid vaules are 'gb', 'mb'.

`--poll-rate RATE` or `-r RATE`, Set info polling rate.

`--version` or `-v`, Print FetchCord Version.

`--config-path CONFIG_PATH` or `-c CONFIG_PATH`, Specify custom neofetch config path.

`--fetchcord-config-path FETCHCORD_CONFIG_PATH` or `-fc FETCHCORD_CONFIG_PATH`, Specify custom fetchcord config path.

`--nfco NFCO` or `-nfco NFCO`, nfco.

`-h` or `--help`, shows this information above.

## Website

Fetchcord now has a website! You can find this site over at [https://fetchcord.github.io/](https://fetchcord.github.io/) - please keep in mind this site is still currently a work in progress though and will have a proper domain soon.

## Examples

### Operating Systems
![MacOS Big Sur](Examples/mac.png) ![Windows 10](Examples/windows.png) ![Ubuntu](Examples/ubuntu.png)
### Terminals
![Konsole](Examples/konsole.png) ![Gnome Terminal](Examples/gnometerm.png) ![Apple Terminal](Examples/appleterm.png)
### CPUs
![Ryzen 9](Examples/ryzencpu.png) ![Intel i7](Examples/intelcpu.png) ![Intel Pentium](Examples/pent.png)
### Hosts
![HP Laptop](Examples/hp.png) ![TUF Gaming Laptop](Examples/tuf.png) ![Lenovo Desktop](Examples/len.png)
