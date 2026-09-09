<h1 align="center">FetchCord</h1>

<p align="center">
  Display your system information as Discord Rich Presence.
</p>

<p align="center">
  <a href="https://github.com/fetchcord/FetchCord">
    <img alt="Linux, macOS, and Windows" src="https://img.shields.io/badge/Compatible-macOS%20%2F%20Linux%20%2F%20Windows-brightgreen?style=for-the-badge&logo=checkmarx&logoColor=white">
  </a>
  <a href="https://www.python.org/downloads/">
    <img alt="Python 3.12+" src="https://img.shields.io/badge/python-3.12%2B-blue.svg?style=for-the-badge&logo=python&logoColor=white">
  </a>
  <a href="https://discord.gg/P4h9kdV">
    <img alt="Discord" src="https://img.shields.io/discord/742068289278312549?label=Discord&logo=discord&logoColor=white&style=for-the-badge">
  </a>
  <a href="LICENSE">
    <img alt="MIT License" src="https://img.shields.io/badge/license-MIT-lightgrey?style=for-the-badge">
  </a>
</p>

<p align="center">
  <img src="Examples/ubuntu.png" alt="FetchCord showing Ubuntu as Discord Rich Presence">
</p>

FetchCord 3 reads system info (primarily through [fastfetch](https://github.com/fastfetch-cli/fastfetch)), then cycles it through Discord Rich Presence: OS and kernel, CPU/GPU/memory, terminal and shell, then host and display.

Discord's desktop client must be running. FetchCord talks to it over local RPC; there is no bot to invite.

## Table of contents

- [What's new in 3.0.0](#whats-new-in-300)
- [Features](#features)
- [Requirements](#requirements)
- [Installing](#installing)
  - [Linux](#linux)
  - [macOS](#macos)
  - [Windows](#windows)
- [Running](#running)
- [Configuration](#configuration)
- [Arguments](#arguments)
- [Updating the icon database](#updating-the-icon-database)
- [Development](#development)
- [Examples](#examples)
- [Website](#website)
- [License](#license)

## What's new in 3.0.0

FetchCord was rewritten around fastfetch and a smaller Python package.

**Breaking**

- Python **3.12+** is required.
- **fastfetch** replaces neofetch on Linux and macOS.
- The old `computer/` package and the Qt GUI are gone.

**Also new**

- Modular layout: config, fetch providers, presence cycles, and a JSON icon database.
- `pyproject.toml` packaging, type hints, and a pytest suite (plus a real fastfetch CI smoke job).
- Windows can run without fastfetch; PowerShell/native fallbacks fill the gaps.

## Features

- OS / distro detection on Linux, macOS, and Windows
- Kernel and package count
- CPU, GPU, and memory, rotated with the other cycles
- Terminal, shell, and font
- Motherboard / host and display resolution
- Laptop vs desktop icon
- User systemd unit on Linux
- `--update` refreshes the distro/CPU/GPU/motherboard icon maps from this repo
- Uptime as Discord's elapsed timer (time since boot)

If an OS, CPU, GPU, terminal, or board has no matching icon, FetchCord still runs and falls back to a generic image. Open a [hardware / distro request](https://github.com/fetchcord/FetchCord/issues/new/choose) to add one.

## Requirements

| | Linux | macOS | Windows |
| --- | --- | --- | --- |
| Python | 3.12+ | 3.12+ | 3.12+ |
| fastfetch | required | required | optional |
| Discord desktop | required | required | required |

On Debian/Ubuntu 24.04+, distro `pip` is externally managed. Use [pipx](https://pipx.pypa.io/) or a virtualenv, not `sudo pip`.

## Installing

**Do not `pip install fetchcord` from PyPI for 3.0.** PyPI still publishes **2.7.7** (neofetch, Python 3.6+). 3.0.0 is not on PyPI yet. Install from this GitHub repository until a `v3.0.0` tag is published there.

The same applies to most distro packages: they still track 2.x unless noted otherwise.

### Linux

Install Python 3.12+ and fastfetch, then:

```bash
pipx install "git+https://github.com/fetchcord/FetchCord.git"
# or, in a virtualenv:
pip install "git+https://github.com/fetchcord/FetchCord.git"
```

That tracks **master** (FetchCord 3). For the development branch:

```bash
pipx install "git+https://github.com/fetchcord/FetchCord.git@testing"
```

Uninstall with `pipx uninstall fetchcord` or `pip uninstall fetchcord`.

**AUR** ([fetchcord](https://aur.archlinux.org/packages/fetchcord/), [fetchcord-testing](https://aur.archlinux.org/packages/fetchcord-testing/)) still packages FetchCord 2.x / neofetch. Prefer pipx from this repo until those packages are updated for 3.0.

**Snap** is not a 3.0 install path. The listing is unmaintained (classic/core18 cannot ship Python 3.12).

**From a clone**

```bash
git clone https://github.com/fetchcord/FetchCord.git
cd FetchCord
pipx install .
```

### macOS

**Requirements: Python 3.12+ and fastfetch.**

Homebrew is the easiest way to get fastfetch. The live tap may still bottle 2.7.7; until a `v3.0.0` tag fills `url`/`sha256` on the formula, install HEAD:

```bash
brew tap fetchcord/fetchcord
brew install --HEAD fetchcord
```

That pulls `fastfetch` and Python 3.12. To build the formula from this repo:

```bash
brew install --HEAD --build-from-source ./Formula/fetchcord.rb
```

**Via pipx** (same as Linux; 3.0 is not on PyPI yet):

```bash
pipx install "git+https://github.com/fetchcord/FetchCord.git"
```

Uninstall with `brew uninstall fetchcord`, or `pipx uninstall fetchcord` / `pip uninstall fetchcord` if you installed with pip.

### Windows

**Requirements: Python 3.12+.** fastfetch is optional.

```bat
py -3.12 -m pip install "git+https://github.com/fetchcord/FetchCord.git"
```

Standalone `FetchCord.exe` builds are attached to GitHub Releases when a `v3.x` tag is published. There is no `v3.0.0` release asset yet.

## Running

Start Discord, then:

```bash
fetchcord
```

If the command is not found, add `~/.local/bin` (Linux/macOS) or your Python `Scripts` directory (Windows) to `PATH`, or run:

```bash
python3 -m fetch_cord
```

FetchCord keeps running until you stop it (`Ctrl+C`). It is safe to launch at login with any autostart method you already use.

### systemd user unit (Linux)

```bash
fetchcord --install
```

That installs `fetchcord.service` into `~/.local/share/systemd/user/` and enables it. Equivalent by hand:

```bash
mkdir -p ~/.local/share/systemd/user
cp systemd/fetchcord.service ~/.local/share/systemd/user/
systemctl --user enable --now fetchcord
```

Extra flags belong in a drop-in, not in the unit from git:

```bash
systemctl --user edit fetchcord
```

```ini
[Service]
ExecStart=
ExecStart=-/usr/bin/env fetchcord --nohost --time 15
```

`--enable`, `--disable`, `--start`, `--stop`, `--status`, and `--uninstall` wrap the matching `systemctl --user` operations. They are Linux-only.

## Configuration

Presence cycles ship in [`fetch_cord/resources/fetchcord_conf.yml`](fetch_cord/resources/fetchcord_conf.yml). There is no separate user config file yet; edit that YAML if you installed from a clone, or override cycles from the CLI.

Default cycles:

| Cycle | Hidden by | Large image | Lines |
| --- | --- | --- | --- |
| `os` | `--nodistro` | distro / OS | kernel, packages |
| `hardware` | `--nohardware` | CPU | memory, GPU |
| `shell` | `--noshell` | terminal | font, shell |
| `host` | `--nohost` | motherboard | motherboard, resolution |

Each cycle has a duration (`time`, default 30 seconds). `--time` / `-t` overrides every cycle; the minimum is 15 seconds.

Each cycle maps:

- `app_id` — which detected value selects the Discord application / large icon (`os`, `cpu`, `terminal`, `motherboard`)
- `top_line` / `bottom_line` — Rich Presence details/state fields
- `small_icon` — small image (`gpu`, `shell`, `system_type`, …)

Available fields include `os`, `kernel`, `packages`, `cpu`, `gpu`, `mem` (alias of `memory`), `shell`, `terminal`, `font`, `motherboard`, `host`, `resolution`, and `system_type`.

## Arguments

| Flag | Description |
| --- | --- |
| `--nodistro` | Skip the OS cycle |
| `--nohardware` | Skip the hardware cycle |
| `--noshell` | Skip the terminal/shell cycle |
| `--nohost` | Skip the host cycle |
| `-t`, `--time TIME` | Cycle length in seconds (minimum 15) |
| `--install` | Install and enable the systemd user service (Linux) |
| `--uninstall` | Remove the systemd user service (Linux) |
| `--enable` / `--disable` | Enable or disable the user service (Linux) |
| `--start` / `--stop` | Start or stop the user service (Linux) |
| `--status` | Print user service status (Linux) |
| `--update` | Download the latest icon JSON files from GitHub |
| `--testing` | With `--update` or `--install`, fetch files from the `testing` branch instead of `master` |
| `-d`, `--debug` | Print detection and RPC details |
| `-v`, `--version` | Print the FetchCord version |
| `-h`, `--help` | Show help |

`--update`, `--version`, and the systemd flags exit after they finish; they do not start Rich Presence.

## Updating the icon database

```bash
fetchcord --update
```

This overwrites the packaged JSON maps (`cpus.json`, `gpus.json`, `os.json`, `terminal.json`, `shell.json`, `motherboards.json`, `system_types.json`) with the copies on `master`. Add `--testing` to pull from the `testing` branch instead.

## Development

```bash
git clone https://github.com/fetchcord/FetchCord.git
cd FetchCord
pip install -e ".[dev]"
ruff check .
mypy fetch_cord tests
python -m pytest tests/ -v
```

CI runs those checks on Python 3.12, 3.13, and 3.14, plus a smoke job that runs real fastfetch.

On a machine with fastfetch (and optionally Discord):

```bash
python scripts/validate.py           # core fields present
python scripts/validate.py --json    # also dump fastfetch JSON
python scripts/validate.py --connect # also set Rich Presence
```

## Examples

### Operating systems

![macOS Big Sur](Examples/mac.png) ![Windows 10](Examples/windows.png) ![Ubuntu](Examples/ubuntu.png)

### Terminals

![Konsole](Examples/konsole.png) ![GNOME Terminal](Examples/gnometerm.png) ![Apple Terminal](Examples/appleterm.png)

### CPUs

![Ryzen 9](Examples/ryzencpu.png) ![Intel i7](Examples/intelcpu.png) ![Intel Pentium](Examples/pent.png)

### Hosts

![HP laptop](Examples/hp.png) ![TUF Gaming laptop](Examples/tuf.png) ![Lenovo desktop](Examples/len.png)

## Website

<https://fetchcord.github.io/> is still a work-in-progress remaster and documents 2.x in places. This README is the source of truth for 3.0.

## License

MIT. See [LICENSE](LICENSE).

Questions and icon requests: [Discord](https://discord.gg/P4h9kdV) or [GitHub Issues](https://github.com/fetchcord/FetchCord/issues).
