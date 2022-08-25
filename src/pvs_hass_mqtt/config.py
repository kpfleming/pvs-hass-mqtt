from __future__ import annotations

import importlib.resources
import logging
import pathlib
import sys
from collections.abc import Mapping
from typing import Any

import yaml
from attrs import define, field
from cerberus import Validator  # type: ignore

logger = logging.getLogger(__name__)


@define(kw_only=True)
class PVS:
    name: str
    url: str
    poll_interval: int


@define(kw_only=True)
class Panel:
    serial: str


@define(kw_only=True)
class Array:
    name: str
    azimuth: float | None
    tilt: float | None
    panel: list[Panel] = field(factory=list)


class ConfigValidationError(Exception):
    def __init__(self, message: str, errors: Mapping[str, Any] | None) -> None:
        self.message: str = message
        self.errors: Mapping[str, Any] | None = errors

    def __str__(self) -> str:
        return self.message


def prettify_errors(errors: Mapping[str, Any], indent: int = 0) -> str:
    # This function originated in the insteon-mqtt project.
    """This creates a nice presentation of the errors for the user

    The error list looks a lot like the YAML document.  Running it through
    yaml.dump() was ok.  However, doing it this way allows us to have
    multiline error messages with nice indentations and such.
    """
    error_msg = ""
    for key in errors.keys():
        error_msg += " " * indent + str(key) + ": \n"
        for item in errors[key]:
            if isinstance(item, dict):
                error_msg += prettify_errors(item, indent=indent + 2)
            else:
                item = item.replace("\n", "\n  " + " " * (indent + 2))
                error_msg += " " * (indent) + "- " + str(item) + "\n"
    return error_msg


@define(kw_only=True)
class Config:
    pvs: list[PVS] = field(factory=list)
    array: list[Array] = field(factory=list)

    @classmethod
    def _from_dict(cls, source: Mapping[Any, Any]) -> Config:
        schema = yaml.safe_load(
            importlib.resources.read_text(sys.modules["pvs_hass_mqtt"], "config-schema.yaml")
        )

        v = Validator(schema)
        if not v.validate(source):
            raise ConfigValidationError(prettify_errors(v.errors), v.errors)

        config = Config()
        panel_serials: set[str] = set()

        for name, pvs in v.document["pvs"].items():
            config.pvs.append(PVS(name=name, url=pvs["url"], poll_interval=pvs["poll_interval"]))

        for name, array in v.document["array"].items():
            ary = Array(name=name, azimuth=array.get("azimuth", None), tilt=array.get("tilt", None))
            config.array.append(ary)
            for serial in array["panel"]:
                if serial in panel_serials:
                    raise ConfigValidationError(f"Panel '{serial}' defined more than once", None)

                ary.panel.append(Panel(serial=serial))
                panel_serials.add(serial)

        return config

    @classmethod
    def from_file(cls, file: pathlib.Path) -> Config:
        try:
            config = cls._from_dict(yaml.safe_load(file.read_text(encoding="utf-8")))
            return config
        except ConfigValidationError as exc:
            exc.message = f"{file}: \n" + exc.message
            raise exc
