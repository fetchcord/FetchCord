from .computer.Computer import Computer
from typing import Dict


class Cycle:
    name: str

    top_line: str = None
    bottom_line: str = None
    small_icon: str = None

    def __init__(self, name: str, config: Dict[str, str], computer: Computer):
        self.name = name

        if "top_line" in config["top_line"]:
            self.top_line = config["top_line"]
        if "bottom_line" in config["bottom_line"]:
            self.bottom_line = config["bottom_line"]
        if "small_icon" in config["small_icon"]:
            self.small_icon = config["small_icon"]