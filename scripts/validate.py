#!/usr/bin/env python3
"""Real-machine validation for FetchCord hardware detection & rich presence.

Run this on a machine that has fastfetch installed (and, for --connect, a
running Discord desktop client):

    python scripts/validate.py                # check hardware detection
    python scripts/validate.py --json         # also dump raw fastfetch JSON
    python scripts/validate.py --connect      # also try to set Discord presence

Exit code is 0 when all core detection fields (os, kernel, cpu, memory) are
present, so it can be used as a quick pass/fail smoke check on real hardware.
"""

from __future__ import annotations

import argparse
import platform
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fetch_cord.config import Config
from fetch_cord.constants import RESULT_NOT_FOUND
from fetch_cord.fetch import (
    CommandProvider,
    FastfetchProvider,
    Fetch,
    get_component_id,
    get_infos,
)
from fetch_cord.info import FASTFETCH_MODULES
from fetch_cord.presence import build_presence_activity

CORE_FIELDS = ("os", "kernel", "cpu", "memory")


def build_command_map(config: Config) -> dict[str, str]:
    os_type = platform.system()
    return {
        component: scripts[os_type]
        for component, scripts in config["commands"].items()
        if os_type in scripts
    }


def build_cycle_payload(
    snapshot: dict[str, str],
    cycle: dict[str, Any],
    fetchcord_ids: dict[str, dict[str, list[str]]],
) -> tuple[str, dict[str, Any]]:
    app = snapshot.get(cycle["app_id"], RESULT_NOT_FOUND)
    bottom = snapshot.get(cycle["bottom_line"], RESULT_NOT_FOUND)
    top = snapshot.get(cycle["top_line"], RESULT_NOT_FOUND)
    icon = snapshot.get(cycle["small_icon"], RESULT_NOT_FOUND)

    client_id = get_component_id(app.lower(), fetchcord_ids[cycle["app_id"]])
    icon_id = get_component_id(icon, fetchcord_ids[cycle["small_icon"]])

    large_image = "big"
    if icon and "apple m" in icon.lower():
        large_image = icon.lower().replace(" ", "-")

    payload = build_presence_activity(
        details=top,
        state=bottom,
        large_image=large_image,
        large_text=app,
        small_image=icon_id,
        small_text=icon,
        start=0,
    )
    return client_id, payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="dump raw fastfetch JSON")
    parser.add_argument(
        "--connect", action="store_true", help="try to set Discord Rich Presence"
    )
    args = parser.parse_args()

    if args.json:
        from fetch_cord.tools import run_command

        print(
            run_command(
                [
                    "fastfetch",
                    "--format",
                    "json",
                    "--structure",
                    ":".join(FASTFETCH_MODULES),
                ]
            )
        )
        return 0

    config = Config()
    config["commands"] = Config("fetchcord_cmds.yml")["commands"]
    fetch = Fetch([FastfetchProvider(), CommandProvider(build_command_map(config))])
    snapshot = fetch.snapshot()

    print("=== Hardware detection ===")
    for field in sorted(snapshot):
        print(f"  {field:<12} {snapshot[field]!r}")

    missing = [field for field in CORE_FIELDS if not snapshot.get(field)]
    print()
    if missing:
        print(f"[WARN] Missing core fields: {', '.join(missing)}")
    else:
        print("[OK] Core hardware detection fields present")

    fetchcord_ids = {
        "os": get_infos("os"),
        "cpu": get_infos("cpus"),
        "gpu": get_infos("gpus"),
        "terminal": get_infos("terminal"),
        "shell": get_infos("shell"),
        "motherboard": get_infos("motherboards"),
        "system_type": get_infos("system_types"),
    }

    payloads: dict[str, tuple[str, dict[str, Any]]] = {}
    print("\n=== Rich Presence payloads (per configured cycle) ===")
    for cycle in config["cycles"]:
        client_id, payload = build_cycle_payload(snapshot, cycle, fetchcord_ids)
        payloads[cycle.get("name", "?")] = (client_id, payload)
        print(f"\n  cycle: {cycle.get('name')}  client_id={client_id}")
        for key, value in payload.items():
            print(f"    {key:<12} {value!r}")

    if args.connect:
        import time

        from pypresence import Presence

        first_name, (client_id, payload) = next(iter(payloads.items()))
        print(
            f"\nConnecting to Discord (cycle '{first_name}', client_id={client_id})..."
        )
        rpc = Presence(int(client_id))
        rpc.connect()
        rpc.update(**payload)
        print(
            "[OK] Rich presence set. Look at your Discord profile. Press Ctrl+C to stop."
        )
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            rpc.clear()
            rpc.close()
            print("\nRich presence cleared.")

    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
