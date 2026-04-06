#!/usr/bin/env python3


from threading import Event
from typing import Dict
from pypresence import Presence, exceptions
import psutil
import time


class Cycle:
    name: str

    app_id: str = None
    top_line: str = None
    bottom_line: str = None
    small_icon: str = None
    time: str = None

    debug: bool = False
    rpc: Presence = None

    stop: Event = None

    def __init__(self, config: Dict, stop: Event = None):
        if stop is None:
            stop = Event()

        for key in config:
            setattr(self, key, config[key])
        self.stop = stop

    def __del__(self) -> None:
        self.close_connection()

    def setup(self, client_id: str) -> None:
        self.rpc = Presence(int(client_id))

    def try_connect(self) -> None:
        while not self.stop.is_set():
            try:
                if self.debug:
                    print('try_connect(name="{}")'.format(self.name))
                self.rpc.connect()
                break
            except ConnectionRefusedError:
                print(
                    """
RPC connection refused (is Discord open?); trying again in 30 seconds"""
                )
                self.wait(30)

    def close_connection(self) -> None:
        """Fully close the RPC connection and ensure cleanup."""
        if self.rpc is not None:
            try:
                self.rpc.clear()
            except Exception as e:
                if self.debug:
                    print(f'close_connection: clear() failed: {e}')
            try:
                self.rpc.close()
            except Exception as e:
                if self.debug:
                    print(f'close_connection: close() failed: {e}')
            self.rpc = None
            time.sleep(0.1)

    def update(
        self, client_id: str, app: str, bottom: str, top: str, icon: str, icon_id: str, large_image: str = "big"
    ):
        try:
            self.rpc.update(
                state=bottom,
                details=top,
                large_image=large_image,
                large_text=app,
                small_image=icon_id,
                small_text=icon,
                start=psutil.boot_time(),
            )

            self.wait(int(self.time)) if self.time else self.wait(30)

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

    def wait(self, n: float, interval_duration: float = 0.05) -> None:
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
