#!/usr/bin/env python3

import json
import platform
import re
from importlib.resources import files
from typing import Protocol

from fetch_cord import resources
from fetch_cord.constants import RESULT_NOT_FOUND, UNKNOWN_COMPONENT_ID
from fetch_cord.info import FASTFETCH_MODULES, parse_fastfetch_json
from fetch_cord.native import native as native_module
from fetch_cord.tools import BashError, exec_bash, exec_ps1, run_command

# Fastfetch reports the Python interpreter (or this app's process) as the
# terminal/shell when FetchCord is launched as `python -m fetch_cord`.
_PYTHONISH_PROCESS = re.compile(r"^(python\d*(\.\d+)?|hermes)$", re.I)


def get_infos(name: str) -> dict[str, list[str]]:
    """Load a component-id database (e.g. ``cpus.json``) from the package data."""
    data_text = (files(resources) / f"{name}.json").read_text()
    data: dict[str, list[str]] = json.loads(data_text)
    return data


# Hardware doesn't change between cycles, so an unmatched component would
# otherwise reprint the same warning every rotation, forever.
_WARNED_UNKNOWN: set[str] = set()


def resolve_component_id(
    search: str, id_list: dict[str, list[str]]
) -> tuple[str, bool]:
    """Look up a component id, and say whether it actually matched.

    Split out from :func:`get_component_id` so callers that want to report on
    a miss - rather than warn about it - can tell a real match from the
    fallback without parsing stdout. Deliberately silent: the warning, and
    the once-only bookkeeping that goes with it, belong to get_component_id.
    """
    for id, patterns in id_list.items():
        if not isinstance(patterns, list):
            continue
        if any(re.search(pattern, search) for pattern in patterns):
            return id, True

    for id, patterns in id_list.items():
        if isinstance(patterns, list) and "unknown" in patterns:
            return id, False

    return UNKNOWN_COMPONENT_ID, False


def get_component_id(search: str, id_list: dict[str, list[str]]) -> str:
    component_id, matched = resolve_component_id(search, id_list)
    if not matched and search not in _WARNED_UNKNOWN:
        _WARNED_UNKNOWN.add(search)
        print(f"Warning: No match found for '{search}'")
    return component_id


def _looks_like_python_process(value: str) -> bool:
    base = value.strip().split()[0]
    base = base.rsplit("/", 1)[-1]
    return bool(_PYTHONISH_PROCESS.match(base))


class FieldProvider(Protocol):
    """A source of system-info fields. Later providers only fill gaps left by
    earlier ones, so adding a provider (e.g. for GPU/LLM) is additive."""

    name: str

    def fetch(self, skip: set[str] | None = None) -> dict[str, str]: ...


class FastfetchProvider:
    """Runs fastfetch once with structured JSON output and maps its modules to
    fields. Returns {} if fastfetch is not installed, so the command provider
    below can take over (e.g. on Windows)."""

    name = "fastfetch"

    def __init__(self, binary: str = "fastfetch") -> None:
        self.binary = binary

    def fetch(self, skip: set[str] | None = None) -> dict[str, str]:
        try:
            raw = run_command(
                [
                    self.binary,
                    "--format",
                    "json",
                    "--structure",
                    ":".join(FASTFETCH_MODULES),
                ]
            )
        except (FileNotFoundError, BashError):
            # Not installed, or wedged and killed by the timeout - either way
            # the command provider below takes over.
            return {}
        fields = parse_fastfetch_json(raw)
        # Drop interpreter-as-terminal so CommandProvider can use $TERM_PROGRAM.
        for key in ("terminal", "shell"):
            value = fields.get(key)
            if value and _looks_like_python_process(value):
                del fields[key]
        if skip:
            return {k: v for k, v in fields.items() if k not in skip}
        return fields


class CommandProvider:
    """Runs per-OS shell commands for fields fastfetch doesn't cover (e.g.
    motherboard, resolution, system_type) or when fastfetch is unavailable."""

    name = "commands"

    def __init__(self, commands: dict[str, str]) -> None:
        # commands: {field: shell_command}, already filtered for this OS.
        self.commands = commands

    def fetch(self, skip: set[str] | None = None) -> dict[str, str]:
        fields: dict[str, str] = {}
        for field, script in self.commands.items():
            if skip and field in skip:
                continue
            try:
                value = (
                    exec_ps1(script)
                    if platform.system() == "Windows"
                    else exec_bash(script)
                )
            except BashError:
                continue
            if value:
                fields[field] = value.split("\n")[0].strip()
        return fields


class NativeProvider:
    """Uses the bundled native (Windows) fetchers, which read the registry and
    Win32 directly. Adds no tool dependency and no subprocess, and returns {}
    for anything it cannot read so another provider fills the gap."""

    name = "native"
    NATIVE_COMPONENTS = (
        "cpu",
        "host",
        "kernel",
        "mem",
        "motherboard",
        "os",
        "packages",
    )

    def __init__(self) -> None:
        self._native = native_module

    def fetch(self, skip: set[str] | None = None) -> dict[str, str]:
        fields: dict[str, str] = {}
        for component in self.NATIVE_COMPONENTS:
            if skip and component in skip:
                continue
            value = self._native.fetch(component)
            if value:
                fields[component] = value
        return fields


class Fetch:
    """Collects system info from a chain of providers and caches the result.

    Call `snapshot()` once per refresh to collect every field, then read
    individual values with `fetch(field)` from the cached snapshot.
    """

    def __init__(self, providers: list[FieldProvider]) -> None:
        self.providers = providers
        self._cache: dict[str, str] = {}

    def snapshot(self) -> dict[str, str]:
        data: dict[str, str] = {}
        for provider in self.providers:
            for field, value in provider.fetch(skip=set(data)).items():
                data.setdefault(field, value)
        # Hardware cycle reads `mem`; fastfetch emits `memory`.
        if "memory" in data and "mem" not in data:
            data["mem"] = data["memory"]
        self._cache = data
        return data

    def fetch(self, field: str | None) -> str:
        if field is None:
            return RESULT_NOT_FOUND
        if field not in self._cache:
            self.snapshot()
        return self._cache.get(field, RESULT_NOT_FOUND)
