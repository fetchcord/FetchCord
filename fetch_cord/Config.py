#!/usr/bin/env python3

import yaml

from fetch_cord.Tools import get_resource_path


class Config(dict):
    def __init__(self, config_name: str = "fetchcord_conf.yml") -> None:
        super(Config, self).__init__(
            self.get_config(get_resource_path("fetch_cord.resources", config_name))
        )

    def get_config(self, path: str):
        with open(path, "r") as stream:
            try:
                return yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

        return None
