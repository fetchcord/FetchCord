#!/usr/bin/env python3

import platform
import json
import re
from pathlib import Path
from typing import Dict

from fetch_cord import resources
from fetch_cord.Tools import exec_bash, exec_ps1, get_resource_path


def get_infos(name: str):
    module_path = Path(resources.__file__).parent
    file_path = module_path / f"{name}.json"
    with file_path.open() as f:
        return json.load(f)


def get_component_id(search: str, id_list: dict) -> str:
    for id, patterns in id_list.items():
        if any(re.search(pattern, search) for pattern in patterns):
            return id
    return id_list["unknown"]


class Fetch:
    scripts: Dict

    def __init__(self, scripts: Dict):
        self.scripts = scripts

    def run_script(self, component_class: str) -> str:
        path = get_resource_path(
            f"fetch_cord.resources.scripts.{platform.system()}", "."
        ).joinpath(component_class)

        if component_class.split(".")[-1].lower() == "ps1":
            return exec_ps1(path)
        else:
            return exec_bash(path)

    def fetch(self, component_class: str) -> str:
        for script in self.scripts[platform.system()][component_class]:
            result = self.run_script(script)

            if result != "":
                return result.lstrip().split("\n")[0]

        return "Not Found"
