#!/usr/bin/env python3

from importlib import resources
import yaml


class Config(dict):
    def __init__(self) -> None:
        super(Config, self).__init__(
            self.get_config(
                self.get_resource_path("fetch_cord.resources", "fetchcord_conf.yml")
            )
        )

    def get_resource_path(self, package, resource: str):
        with resources.path(package, resource) as path:
            return path

        return None

    def get_config(self, path: str):
        with open(path, "r") as stream:
            try:
                return yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

        return None
