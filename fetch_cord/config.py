#!/usr/bin/env python3

from pathlib import Path
from typing import Any

import yaml

from fetch_cord.tools import get_resource_path


class Config(dict[str, Any]):
    def __init__(self, config_name: str = "fetchcord_conf.yml") -> None:
        data = self.get_config(get_resource_path("fetch_cord.resources", config_name))
        if data is None:
            raise ValueError(f"Failed to parse YAML config: {config_name}")
        super().__init__(data)

    def get_config(self, path: str | Path) -> dict[str, Any] | None:
        with open(path) as stream:
            try:
                data = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
                return None

        if not isinstance(data, dict):
            raise ValueError("Config root must be a mapping")
        return data
