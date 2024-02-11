#!/usr/bin/env python3

import platform
import json
import re
from pathlib import Path
from typing import Dict

from fetch_cord import resources
from fetch_cord.Tools import exec_bash, exec_ps1


def get_infos(name: str):
    module_path = Path(resources.__file__).parent
    file_path = module_path / f"{name}.json"
    with file_path.open() as f:
        return json.load(f)


def get_component_id(search: str, id_list: dict) -> str:
    for id, patterns in id_list.items():
        if any(re.search(pattern, search) for pattern in patterns):
            return id

    for id, patterns in id_list.items():
        if "unknown" in patterns:
            return id

    return "unknown"


class Fetch:
    scripts: Dict

    def __init__(self, scripts: Dict):
        self.scripts = scripts

    def run_script(self, script: str) -> str:
        if platform.system() == "Windows":
            return exec_ps1(script)
        else:
            return exec_bash(script)

    def fetch(self, component_class: str) -> str:
        if component_class not in self.scripts:
            return f"Error: Component {component_class} not found"

        result = self.run_script(self.scripts[component_class])

        if result != "":
            return result.lstrip().split("\n")[0]

        return "Not Found"
