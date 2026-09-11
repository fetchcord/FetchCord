#!/usr/bin/env python3


import time
from threading import Event
from typing import Any

import psutil
from pypresence import exceptions
from pypresence.presence import Presence

from fetch_cord.constants import (
    DEFAULT_CYCLE_TIME_SECONDS,
    RPC_CONNECTION_REFUSED_MSG,
    WAIT_INTERVAL_SECONDS,
)
from fetch_cord.presence import build_presence_activity


class Cycle:
    name: str
    app_id: str | None = None
    top_line: str | None = None
    bottom_line: str | None = None
    small_icon: str | None = None
    time: int | None = None

    debug: bool = False
    rpc: Presence | None = None
    connected: bool = False

    stop: Event

    def __init__(self, config: dict[str, Any], stop: Event | None = None) -> None:
        if stop is None:
            stop = Event()

        for key in config:
            setattr(self, key, config[key])
        self.stop = stop

    def setup(self, client_id: str) -> None:
        self.rpc = Presence(int(client_id))
        self.connected = False

    def try_connect(self) -> None:
        if self.rpc is None or self.connected:
            return

        while not self.stop.is_set():
            try:
                if self.debug:
                    print(f'try_connect(name="{self.name}")')
                self.rpc.connect()
                self.connected = True
                break
            except (ConnectionRefusedError, exceptions.DiscordNotFound):
                print(RPC_CONNECTION_REFUSED_MSG)
                self.wait(DEFAULT_CYCLE_TIME_SECONDS)

    def close_connection(self) -> None:
        """Fully close the RPC connection and ensure cleanup."""
        if self.rpc is not None:
            try:
                self.rpc.clear()
            except Exception as e:
                if self.debug:
                    print(f"close_connection: clear() failed: {e}")
            try:
                self.rpc.close()
            except Exception as e:
                if self.debug:
                    print(f"close_connection: close() failed: {e}")
            self.rpc = None
            self.connected = False
            time.sleep(0.1)

    def update(
        self,
        app: str,
        bottom: str,
        top: str,
        icon: str,
        icon_id: str,
        large_image: str = "big",
    ) -> None:
        if self.rpc is None:
            return

        try:
            self.rpc.update(
                **build_presence_activity(
                    details=top,
                    state=bottom,
                    large_image=large_image,
                    large_text=app,
                    small_image=icon_id,
                    small_text=icon,
                    start=int(psutil.boot_time()),
                )
            )

            self.wait(self.time if self.time else DEFAULT_CYCLE_TIME_SECONDS)

        except ConnectionResetError as e:
            if self.debug:
                print(f'update: ConnectionResetError for "{self.name}": {e}')
            # Connection was reset - need to reconnect
            self.close_connection()
            raise

        except exceptions.InvalidID as e:
            if self.debug:
                print(f'update: InvalidID for "{self.name}": {e}')
            # Invalid client_id - need to re-setup with new client_id
            self.close_connection()
            raise

    def wait(self, n: float, interval_duration: float = WAIT_INTERVAL_SECONDS) -> None:
        """Wait for n seconds or until interrupted."""

        intervals = int(n / interval_duration)
        for _ in range(intervals):
            if self.stop.wait(interval_duration):
                break

    def __repr__(self) -> str:
        return f"""
{{name = {self.name}, \
app_id = {self.app_id}, \
top_line = {self.top_line}, \
bottom_line = {self.bottom_line}, \
small_icon = {self.small_icon}, \
time = {self.time}}}"""
