import argparse


def parse_args():

    parser = argparse.ArgumentParser(description="Fetch Cord\n"
                                                 "https://github.com/MrPotatoBobx/FetchCord")
    parser.add_argument('--nodistro', action='store_true',
                        help="Don't show distro info.")
    parser.add_argument('--nohardware', action='store_true',
                        help="Don't show hardware info.")
    parser.add_argument('--noshell', action='store_true',
                        help="Don't show shell/terminal info.")
    parser.add_argument('--nohost', action='store_true',
                        help="Don't show host info.")
    parser.add_argument('--time', '-t', metavar='TIME', action='store',
                        help="Set custom time in seconds for cycles. Default is 30 seconds")
    parser.add_argument('--terminal', metavar='TERMINAL', action='store',
                        help="Set custom Terminal (useful if using something like dmenu, or launching from a script).")
    parser.add_argument('--termfont', metavar='TERMFONT', action='store',
                        help="Set ustom Terminal Font (useful if neofetch can't get it).")
    parser.add_argument('--update', action='store_true',
                        help="Update database of distros, hardware, etc.")
    parser.add_argument('--debug', action='store_true',
                        help="Enable debugging.")
    parser.add_argument('--pause-cycle', action='store_true',
                        help="Extra cycle that pauses for 30 seconds or custom time using --time argument.")
    parser.add_argument('--memtype', metavar='TYPE', action='store',
                        help="Show Memory in GiB or MiB. Valid vaules are 'gb', 'mb'")
    parser.add_argument('--config', metavar='PATH', action='store',
                        help="Use custom neofetch dump.")


    return parser.parse_args()
