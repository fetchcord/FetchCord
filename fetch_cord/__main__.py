# from __future__ import annotations

import argparse
import os
import platform
import sys
from signal import SIGINT, SIGTERM, signal
from threading import Event

import psutil
from pypresence import exceptions

from fetch_cord.args import parse_args
from fetch_cord.autostart import handle as handle_autostart
from fetch_cord.config import Config
from fetch_cord.constants import (
    CUSTOM_TIME_MESSAGE,
    DEFAULT_CYCLE_TIME_SECONDS,
    MIN_CYCLE_TIME_SECONDS,
)
from fetch_cord.cycle import Cycle
from fetch_cord.fetch import (
    CommandProvider,
    FastfetchProvider,
    Fetch,
    FieldProvider,
    NativeProvider,
    get_infos,
)
from fetch_cord.presence import ResolvedCycle, parse_buttons, resolve_cycle
from fetch_cord.processes import PauseWatcher
from fetch_cord.resources import systemd_service
from fetch_cord.update import update

from . import VERSION


def handle_args(args: argparse.Namespace) -> None:
    """Handle the arguments passed to the program."""

    if args.update:
        update(testing=args.testing)
    # Autostart works the same way on every platform, so it is handled before
    # the systemd-only block below rather than inside it.
    for flag, action in (
        ("install_startup", "install"),
        ("uninstall_startup", "uninstall"),
        ("startup_status", "status"),
    ):
        if getattr(args, flag, False):
            sys.exit(handle_autostart(action))
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
        try:
            seconds = float(args.time)
        except ValueError:
            print(f"ERROR: --time must be a number, got {args.time!r}.")
            sys.exit(1)
        if seconds < MIN_CYCLE_TIME_SECONDS:
            print(
                f"ERROR: Invalid time set, must be > {MIN_CYCLE_TIME_SECONDS} "
                "seconds, cannot continue."
            )
            sys.exit(1)
        print(CUSTOM_TIME_MESSAGE.format(time=args.time))


def _resolve(
    cycle: Cycle,
    snapshot: dict[str, str],
    fetchcord_ids: dict[str, dict[str, list[str]]],
) -> ResolvedCycle:
    """Adapt a configured Cycle to the shared resolver.

    The None checks in the caller have already run, so the field names are
    known to be set by the time we get here.
    """
    assert cycle.app_id and cycle.top_line and cycle.bottom_line and cycle.small_icon
    return resolve_cycle(
        snapshot,
        fetchcord_ids,
        name=cycle.name,
        app_id=cycle.app_id,
        top_line=cycle.top_line,
        bottom_line=cycle.bottom_line,
        small_icon=cycle.small_icon,
    )


def print_dry_run(resolved: list[ResolvedCycle], start: int) -> None:
    """Print each cycle's Discord app and payload without connecting."""
    for cycle in resolved:
        print(f"\ncycle: {cycle.name}  client_id={cycle.client_id}")
        for key, value in cycle.activity(start).items():
            print(f"  {key:<12} {value!r}")


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
    buttons = parse_buttons(config.get("buttons"))
    for cycle in cycles:
        cycle.debug = args.debug
        cycle.buttons = buttons
        if args.time:
            # handle_args has already validated this parses as a float.
            cycle.time = int(float(args.time))

    # CLI wins over the config file so this is usable without editing the
    # packaged config.
    pause_when = getattr(args, "pause_when", None) or config.get("pause_when") or []
    pause = PauseWatcher(pause_when)

    os_type = platform.system()
    # Only the commands defined for this OS are run.
    command_map = {
        component_type: value[os_type]
        for component_type, value in config["commands"].items()
        if os_type in value
    }

    # Native fetchers first: they need no tool installed and cost a few
    # milliseconds. fastfetch then covers everything native does not implement
    # yet, and the commands cover what neither reaches.
    #
    # This is only safe because a native fetcher returns None when it is not
    # confident rather than guessing - an unreadable registry key, or firmware
    # boilerplate like "To Be Filled By O.E.M." - so Fetch.snapshot hands the
    # field straight to fastfetch. Native coverage can grow one field at a
    # time without any platform ever losing detail it has today.
    providers: list[FieldProvider] = [
        NativeProvider(),
        FastfetchProvider(),
        CommandProvider(command_map),
    ]

    fetch = Fetch(providers)

    if getattr(args, "dry_run", False):
        snapshot = fetch.snapshot()
        print("=== Detected ===")
        for field in sorted(snapshot):
            print(f"  {field:<12} {snapshot[field]!r}")
        print("\n=== Would send ===")
        print_dry_run(
            [_resolve(cycle, snapshot, fetchcord_ids) for cycle in cycles],
            int(psutil.boot_time()),
        )
        return

    def signal_handler(signum: int, frame: object) -> None:
        stop_event.set()
        for cycle in cycles:
            cycle.close_connection()

    signal(SIGINT, signal_handler)
    signal(SIGTERM, signal_handler)

    # Main loop
    current_client_id = None
    while not stop_event.is_set():
        if pause.check():
            # Leave the profile alone so whatever else is running keeps the
            # status it would have had - and skip the snapshot entirely,
            # since a rotation we are not going to send is not worth a dozen
            # PowerShell processes.
            for other in cycles:
                if other.rpc:
                    other.close_connection()
            current_client_id = None
            if cycles:
                cycles[0].wait(cycles[0].time or DEFAULT_CYCLE_TIME_SECONDS)
            else:
                stop_event.wait(DEFAULT_CYCLE_TIME_SECONDS)
            continue

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

            resolved = _resolve(cycle, snapshot, fetchcord_ids)
            app = resolved.app
            bottom = resolved.bottom
            top = resolved.top
            icon = resolved.icon
            client_id = resolved.client_id
            icon_id = resolved.icon_id
            large_image = resolved.large_image

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
