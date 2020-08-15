import argparse


def parse_args():

    parser = argparse.ArgumentParser(description="Fetch Cord\n"
                                                 "https://github.com/MrPotatoBobx/FetchCord")
    parser.add_argument('--distro', action='store_true',
                        help="Show Distro info only or with other arguments.")
    parser.add_argument('--hardware', action='store_true',
                        help="Show Hardware only or with other arguments.")
    parser.add_argument('--shell', action='store_true',
                        help="Show Shell/Terminal only or with other arguments.")
    parser.add_argument('--time', '-t', metavar='TIME', action='store',
                        help="Set custom time in seconds for cycles. Default is 30 seconds")
    parser.add_argument('--debug', action='store_true',
                        help="Enable debugging.")
    parser.add_argument('--termfont', metavar='TERMFONT', action='store',
                        help="Set ustom Terminal Font (useful if neofetch can't get it).")
    parser.add_argument('--terminal', metavar='TERMINAL', action='store',
                        help="Set custom Terminal (useful if using something like dmenu, or launching from a script).")
    parser.add_argument('--host', action='store_true',
                        help="Show Host info only or with other arguments.")
    parser.add_argument('--update', action='store_true',
                        help="Update database.")

    return parser.parse_args()
