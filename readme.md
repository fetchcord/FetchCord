# FetchCord

Fetchcord grabs information about your Distro and displays it as Discord Rich Presence

## Examples

![ubunt_example.png](/home/amir/Documents/code/fetchcord/Examples/ubunt_example.png)

## What works

- [x] Distro detection

- [x] Package detection

- [x] Kernel Detection

- [x] Uptime

- [x] Distro version

## To-Do(What doesn't work)

- [ ] Add distros apps for rich presnse that arent ubuntu or opensuse leap

- [ ] Add more distros

- [ ] Detect wm/de and wm/de version

#### Note: as of now only ubuntu and opensuse leap work, and opensuse leap doesn't show icon(More distros are bing worked on) This is wip as of now.

## Running

To run the scrip simply run `python3  run-rpc.py`, python 3.8 should have the `distro` module but if you get an error install it via pip, `pip3 install distro`


