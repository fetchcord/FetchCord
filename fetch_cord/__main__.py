# from __future__ import annotations

import argparse
import os
import platform
import sys
from signal import SIGINT, SIGTERM, signal
from threading import Event

from pypresence import exceptions

from fetch_cord.args import parse_args
from fetch_cord.config import Config
from fetch_cord.constants import (
    CUSTOM_TIME_MESSAGE,
    MIN_CYCLE_TIME_SECONDS,
    RESULT_NOT_FOUND,
)
from fetch_cord.cycle import Cycle
from fetch_cord.fetch import (
    CommandProvider,
    FastfetchProvider,
    Fetch,
    NativeProvider,
    get_component_id,
    get_infos,
)
from fetch_cord.resources import systemd_service
from fetch_cord.update import update

from . import VERSION


def handle_args(args: argparse.Namespace) -> None:
    """Handle the arguments passed to the program."""

    if args.update:
        update(testing=args.testing)
    if os.name != "nt" and sys.platform != "darwin":
        if args.install:
            systemd_service.install(testing=args.testing)
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
        print("FetchCord version:", VERSION)
        sys.exit(0)
    if args.time:
        if float(args.time) < MIN_CYCLE_TIME_SECONDS:
            print(
                f"ERROR: Invalid time set, must be > {MIN_CYCLE_TIME_SECONDS} "
                "seconds, cannot continue."
            )
            sys.exit(1)
        print(CUSTOM_TIME_MESSAGE.format(time=args.time))


def main(
    args: argparse.Namespace | None = None, *, stop_event: Event | None = None
) -> None:
    """Run FetchCord. Parses CLI args unless one is supplied (embeddable).

    ``stop_event`` is injectable so tests can terminate the loop deterministically;
    it is created internally when not provided.
    """
    if args is None:
        args = parse_args()
    handle_args(args)

    # Get the ids for the components
    fetchcord_ids = {
        "cpu": get_infos("cpus"),
        "gpu": get_infos("gpus"),
        "os": get_infos("os"),
        "terminal": get_infos("terminal"),
        "shell": get_infos("shell"),
        "motherboard": get_infos("motherboards"),
        "system_type": get_infos("system_types"),
    }

    # Stop event for the loop (injectable for tests)
    if stop_event is None:
        stop_event = Event()

    # Load config
    config = Config()
    config["commands"] = Config("fetchcord_cmds.yml")["commands"]
    # Load cycles
    cycles = [Cycle(cycle, stop_event) for cycle in config["cycles"]]

    # Apply CLI overrides: honor --debug / --time and drop disabled cycles.
    hide = {
        "os": args.nodistro,
        "hardware": args.nohardware,
        "shell": args.noshell,
        "host": args.nohost,
    }
    cycles = [c for c in cycles if not hide.get(c.name, False)]
    for cycle in cycles:
        cycle.debug = args.debug
        if args.time:
            cycle.time = int(args.time)

    os_type = platform.system()
    # Only the commands defined for this OS are run. The structured fastfetch
    # provider fills the common fields first; command/native providers only
    # fill the gaps (e.g. motherboard/resolution/system_type, or everything on
    # Windows where fastfetch may not be installed).
    command_map = {
        component_type: value[os_type]
        for component_type, value in config["commands"].items()
        if os_type in value
    }

    fetch = Fetch([FastfetchProvider(), CommandProvider(command_map), NativeProvider()])

    def signal_handler(signum: int, frame: object) -> None:
        stop_event.set()
        for cycle in cycles:
            cycle.close_connection()

    signal(SIGINT, signal_handler)
    signal(SIGTERM, signal_handler)

    # Main loop
    current_client_id = None
    while not stop_event.is_set():
        # Collect every field once per rotation rather than once per cycle.
        # Each cycle reads different fields out of the same snapshot, and on
        # Windows a snapshot is a dozen PowerShell processes.
        snapshot = fetch.snapshot()

        # Loop through the cycles defined in the config
        for cycle in cycles:
            if stop_event.is_set():
                break

            app_id = cycle.app_id
            top_line = cycle.top_line
            bottom_line = cycle.bottom_line
            small_icon = cycle.small_icon
            if (
                app_id is None
                or top_line is None
                or bottom_line is None
                or small_icon is None
            ):
                continue

            app = snapshot.get(app_id, RESULT_NOT_FOUND)
            bottom = snapshot.get(bottom_line, RESULT_NOT_FOUND)
            top = snapshot.get(top_line, RESULT_NOT_FOUND)
            icon = snapshot.get(small_icon, RESULT_NOT_FOUND)

            client_id = get_component_id(app.lower(), fetchcord_ids[app_id])

            icon_id = get_component_id(icon, fetchcord_ids[small_icon])

            # For Apple M chips, use the chip name as the large image
            large_image = "big"
            if icon and "apple m" in icon.lower():
                # Convert "Apple M4 Pro" to "apple-m4-pro"
                large_image = icon.lower().replace(" ", "-")

            if args.debug:
                print(
                    f"""client_id: {client_id} \
app: {app} \
bottom: {bottom} \
top: {top} \
icon: {icon} \
icon_id: {icon_id} \
large_image: {large_image}"""
                )

            # Reconnect if client_id changed
            if client_id != current_client_id:
                # Close ALL cycles' connections since Discord only allows one RP at a time
                for c in cycles:
                    if c.rpc:
                        c.close_connection()
                current_client_id = client_id

            if cycle.rpc is None:
                cycle.setup(client_id)

            cycle.try_connect()

            try:
                cycle.update(app, bottom, top, icon, icon_id, large_image)
            except (ConnectionResetError, exceptions.InvalidID):
                cycle.close_connection()

        stop_event.wait(0.05)

    # stop_event is set by the SIGINT/SIGTERM handler above, which mypy cannot
    # see, so this cleanup runs when the loop is interrupted by a signal.
    for cycle in cycles:
        cycle.close_connection()

    print("Activity cleared and connections closed.")


if __name__ == "__main__":
    main()
