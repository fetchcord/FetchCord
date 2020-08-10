import argparse

def parse_args():

    parser = argparse.ArgumentParser(description="Fetch Cord\n"
                                                 "https://github.com/MrPotatoBobx/FetchCord")
    parser.add_argument('--distro', action='store_true',
            help="Show Distro info only")
    parser.add_argument('--hardware', action='store_true',
            help="Show Hardware only")
    parser.add_argument('--shell', action='store_true',
            help="Show Shell/Terminal only")
    parser.add_argument('--time', '-t', metavar='TIME', action='store',
            help="Set custom time in seconds for cycles. Default is 30 seconds")
    parser.add_argument('--debug', action='store_true',
            help="Enable debugging.")

    return parser.parse_args()
