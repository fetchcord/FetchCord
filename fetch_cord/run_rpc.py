#from __future__ import annotations


from typing import Callable, Dict
from pypresence import Presence, exceptions
import time, sys

# import info about system
from .args import parse_args
from .config import ConfigError, load_config
from .computer.Computer import Computer

args = parse_args()


class Run_rpc:
    rpcs: Dict[str, Presence]
    config: Dict

    loops: Dict[str, Callable[['Run_rpc', str, Computer], None]] # Cannot use Run_rpc for type hinting unless doing the __future__.annotations import
    loops_indexes: Dict[int, str]
    poll_rate: int
    update: Callable

    def __init__(self):
        self.rpcs = {}

        try:
            self.config = load_config()
        except ConfigError as e:
            print("Error loading config file, using default values." % str(e))

    def set_loop(
        self, loops: Dict, loops_indexes: Dict, update: Callable, poll_rate: int = 3
    ):
        self.loops = loops
        self.loops_indexes = loops_indexes

        self.poll_rate = poll_rate
        self.update = update

    def run_loop(self, computer: Computer):
        try:
            loop = 0
            while True:
                for i in range(len(self.loops_indexes)):
                    if loop == self.poll_rate:
                        self.update()
                        loop = 0
                    try:
                        client_id, func = self.loops[self.loops_indexes[i]]

                        if args.debug:
                            print(self.rpcs)
                            print(
                                "{} not in : {}".format(
                                    self.loops_indexes[i],
                                    self.loops_indexes[i] not in self.rpcs,
                                )
                            )
                        if self.loops_indexes[i] not in self.rpcs:
                            self.rpcs[self.loops_indexes[i]] = Presence(client_id)
                        self.try_connect(self.loops_indexes[i])

                        func(self, self.loops_indexes[i], computer)
                        loop += 1
                    except ConnectionResetError:
                        self.try_connect(self.loops_indexes[i])
        except KeyboardInterrupt:
            print("Closing connection.")
            sys.exit(0)

    def try_connect(self, key: str):
        while True:
            try:
                if args.debug:
                    print('try_connect(key="{}") on {}'.format(key, self.rpcs[key]))
                self.rpcs[key].connect()
                break
            except ConnectionRefusedError:
                print(
                    "RPC connection refused (is Discord open?); trying again in 30 seconds"
                )
                time.sleep(30)

    def try_clear(self, key: str):
        # Pypresence clear doesn't work anymore
        # try:
        #     if args.debug:
        #         print(
        #             "[key={}] try_clear(pid={} on {}".format(
        #                 key, os.getpid(), self.rpcs[key]
        #             )
        #         )
        #     self.rpcs[key].clear(pid=os.getpid())
        # except exceptions.InvalidID:
        #     pass
        # except exceptions.ServerError as e:
        #     print(e)
        #     pass
        self.rpcs[key].close()

    def try_update(
        self,
        key: str,
        state,
        details,
        large_image,
        large_text,
        small_image,
        small_text,
        start,
    ):
        try:
            if args.debug:
                print('try_update(key="{}") on {}'.format(key, self.rpcs[key]))
            self.rpcs[key].update(
                state=state,
                details=details,
                large_image=large_image,
                large_text=large_text,
                small_image=small_image,
                small_text=small_text,
                start=start,
            )
        # ConnectionResetError is here to avoid crashing if Discord is still just starting
        except (ConnectionResetError, exceptions.InvalidID):
            pass