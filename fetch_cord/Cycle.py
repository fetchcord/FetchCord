# 1/usr/bin/env python3


from threading import Event
from typing import Dict
from pypresence import Presence, exceptions
import psutil


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

    def __init__(self, config: Dict, stop: Event = Event()):
        for key in config:
            setattr(self, key, config[key])
        self.stop = stop

    def __del__(self) -> None:
        if self.rpc is not None:
            self.rpc.close()

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

    def update(self, client_id: str, bottom: str, top: str, icon: str):
        try:
            self.rpc.update(
                int(client_id),
                state=bottom,
                details=top,
                large_image="big",
                large_text=bottom,
                small_image=icon,
                small_text=top,
                start=psutil.boot_time(),
            )

            self.wait(int(self.time))

            self.rpc.close()
        # ConnectionResetError is here to avoid crashing
        # if Discord is still just starting
        except (ConnectionResetError, exceptions.InvalidID):
            pass

    def wait(self, n: float, interval_duration: float = 0.05) -> None:
        """Wait for n seconds or until interrupted."""

        intervals = int(n / interval_duration)
        for i in range(intervals):
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
