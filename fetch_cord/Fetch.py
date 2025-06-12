#!/usr/bin/env python3

import platform
import json
import re
from pathlib import Path
from typing import Dict

from fetch_cord import resources
from fetch_cord.native import native as native_module
from fetch_cord.Tools import exec_bash, exec_ps1
from fetch_cord.get_resources import get_default_config


def get_infos(name: str):
    module_path = Path(resources.__file__).parent
    file_path = module_path / f"{name}.json"
    with file_path.open() as f:
        return json.load(f)


def get_component_id(search: str, id_list: dict) -> str:
    for id, patterns in id_list.items():
        if any(re.search(pattern, search) for pattern in patterns):
            return id

    print(f"Warning: No match found for '{search}' in the provided patterns: {id_list}")
    for id, patterns in id_list.items():
        if "unknown" in patterns:
            return id

    return "unknown"


class Fetch:
    scripts: Dict

    def __init__(self, scripts: Dict):
        self.scripts = scripts

    def run_script(self, script: str) -> str:
        # TODO fastfetch config handling
        # if "neofetch" in script:
        #     script.replace("neofetch", f"neofetch --config {get_default_config()}")

        if platform.system() == "Windows":
            return exec_ps1(script)
        else:
            return exec_bash(script)

    def fetch(self, component_class: str) -> str:
        result = (
            native_module.fetch(component_class)
            if component_class not in self.scripts
            else self.run_script(self.scripts[component_class])
        )

        if result is None:
            return f"Error: Component {component_class} not found"

        if result != "":
            return result.lstrip().split("\n")[0]

        return "Not Found"
