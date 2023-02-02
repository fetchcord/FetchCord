# from __future__ import annotations

import sys, os

from signal import SIGINT, SIGTERM, signal
from threading import Event
from fetch_cord.Config import Config
from fetch_cord.Cycle import Cycle
from fetch_cord.Fetch import Fetch, get_infos, get_component_id
from .update import update
from . import __init__ as __init__
from .resources import systemd_service

from fetch_cord.args import parse_args

args = parse_args()
__all__ = [args]


def handle_args() -> None:
    if args.update:
        update()
    if os.name != "nt" and sys.platform != "darwin":
        if args.install:
            systemd_service.install()
        if args.uninstall:
            systemd_service.uninstall()
        if args.enable:
            systemd_service.enable()
        if args.disable:
            systemd_service.disable()
        if args.start:
            systemd_service.start()
        if args.stop:
            systemd_service.stop()
        if args.status:
            systemd_service.status()
    if args.version:
        print("FetchCord version:", __init__.VERSION)
        sys.exit(0)
    if args.time:
        if int(args.time) < 15:
            print("ERROR: Invalid time set, must be > 15 seconds, cannot continue.")
            sys.exit(1)
        else:
            print("setting custom time %s seconds" % args.time)
    try:
        if args.help:
            sys.exit(0)
    except AttributeError:
        pass


def main():
    handle_args()

    fetchcord_ids = {
        "cpu": get_infos("cpus"),
        "gpu": get_infos("gpus"),
        "os": get_infos("os"),
        "motherboard": get_infos("motherboards"),
        "system_type": get_infos("system_types"),
    }

    # Stop event for the loop
    stop_event = Event()

    # Load config
    config = Config()
    # Load cycles
    cycles = [Cycle(cycle, stop_event) for cycle in config["cycles"]]
    fetch = Fetch(config["scripts"])

    signal(SIGINT, lambda s, f: stop_event.set())
    signal(SIGTERM, lambda s, f: stop_event.set())

    while not stop_event.is_set():
        for cycle in cycles:
            if stop_event.is_set():
                break

            app = fetch.fetch(cycle.app_id)
            bottom = fetch.fetch(cycle.bottom_line)
            top = fetch.fetch(cycle.top_line)
            icon = fetch.fetch(cycle.small_icon)

            client_id = get_component_id(app.lower(), fetchcord_ids[cycle.app_id])

            icon_id = get_component_id(icon, fetchcord_ids[cycle.small_icon])

            print(
                f"""client_id: {client_id} \
app: {app} \
bottom: {bottom} \
top: {top} \
icon: {icon} \
icon_id: {icon_id}"""
            )

            if cycle.rpc is None:
                cycle.setup(client_id)

            try:
                cycle.try_connect()
            except ConnectionResetError:
                cycle.try_connect()

            cycle.update(client_id, bottom, top, icon_id)

        stop_event.wait(0.05)

    print("Closing connection.")


if __name__ == "__main__":
    main()
