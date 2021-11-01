# from __future__ import annotations

import argparse


def parse_args():

    parser = argparse.ArgumentParser(
        description="Fetch Cord\n" "https://github.com/MrPotatoBobx/FetchCord"
    )
    parser.add_argument(
        "--nodistro", action="store_true", help="Don't show distro info."
    )
    parser.add_argument(
        "--nohardware", action="store_true", help="Don't show hardware info."
    )
    parser.add_argument(
        "--noshell", action="store_true", help="Don't show shell/terminal info."
    )
    parser.add_argument("--nohost", action="store_true", help="Don't show host info.")
    parser.add_argument(
        "--noconfig",
        action="store_true",
        help="Disable neofetch custom config. Enable if you have an incompatible custom configuration.",
    )
    parser.add_argument(
        "--time",
        "-t",
        metavar="TIME",
        action="store",
        help="Set custom time in seconds for cycles. Default is 30 seconds",
    )
    parser.add_argument(
        "--terminal",
        metavar="TERMINAL",
        action="store",
        help="Set custom Terminal (useful if using something like dmenu, or launching from a script).",
    )
    parser.add_argument(
        "--termfont",
        metavar="TERMFONT",
        action="store",
        help="Set custom Terminal Font (useful if neofetch can't get it).",
    )
    parser.add_argument(
        "--install",
        action="store_true",
        help="Install fetchcord as a systemd service (user) and enable it.",
    )
    parser.add_argument(
        "--uninstall",
        action="store_true",
        help="Uninstall fetchcord as a systemd service (user).",
    )
    parser.add_argument(
        "--enable",
        action="store_true",
        help="Enable fetchcord systemd service (user).",
    )
    parser.add_argument(
        "--disable",
        action="store_true",
        help="Disable fetchcord systemd service (user).",
    )
    parser.add_argument(
        "--start",
        action="store_true",
        help="Start fetchcord systemd service (user).",
    )
    parser.add_argument(
        "--stop",
        action="store_true",
        help="Stop fetchcord systemd service (user).",
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Get fetchcord systemd service status (user).",
    )
    parser.add_argument(
        "--update",
        action="store_true",
        help="Update database of distros, hardware, etc.",
    )
    parser.add_argument(
        "--testing",
        action="store_true",
        help="Get files from testing branch instead of master.",
    )
    parser.add_argument("--debug", "-d", action="store_true", help="Enable debugging.")
    parser.add_argument(
        "--pause-cycle",
        "-p",
        action="store_true",
        help="Extra cycle that pauses for 30 seconds or custom time using --time argument.",
    )
    parser.add_argument(
        "--memtype",
        "-m",
        metavar="TYPE",
        action="store",
        help="Show Memory in GiB or MiB. Valid vaules are 'gb', 'mb'",
    )
    parser.add_argument(
        "--poll-rate",
        "-r",
        metavar="RATE",
        action="store",
        help="Set info polling rate.",
    )
    parser.add_argument(
        "--version", "-v", action="store_true", help="Print FetchCord Version."
    )
    parser.add_argument(
        "--config-path",
        "-c",
        action="store",
        help="Specify custom neofetch config path.",
    )
    parser.add_argument(
        "--fetchcord-config-path",
        "-fc",
        action="store",
        help="Specify custom fetchcord config path.",
    )
    parser.add_argument(
        "--nfco",
        "-nfco",
        action="store",
        help="nfco",
    )

    return parser.parse_args()
