import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch Cord\nhttps://github.com/fetchcord/FetchCord"
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
        "--time",
        "-t",
        metavar="TIME",
        action="store",
        help="Set custom time in seconds for cycles. Default is 30 seconds",
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
    parser.add_argument(
        "--pause-when",
        metavar="NAME",
        nargs="+",
        help=(
            "Process names that should hold the presence back while they run "
            "(e.g. --pause-when steam spotify). Overrides pause_when in the "
            "config. The .exe suffix is optional."
        ),
    )
    parser.add_argument("--debug", "-d", action="store_true", help="Enable debugging.")
    parser.add_argument(
        "--version", "-v", action="store_true", help="Print FetchCord Version."
    )

    return parser.parse_args()
