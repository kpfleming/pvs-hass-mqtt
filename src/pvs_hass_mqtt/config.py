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
    URL: str


@define(kw_only=True)
class Panel:
    serial: str


@define(kw_only=True)
class Array:
    name: str
    azimuth: float
    tilt: float
    panel: list[Panel] = field(factory=list)


@define(kw_only=True)
class Config:
    pvs: list[PVS] = field(factory=list)
    array: list[Array] = field(factory=list)

    @classmethod
    def _from_dict(cls, config: Mapping[Any, Any]) -> Config:
        schema = yaml.safe_load(
            importlib.resources.read_text(sys.modules["pvs_hass_mqtt"], "config-schema.yaml")
        )
        v = Validator(schema)
        v.validate(config)
        return Config()

    @classmethod
    def from_file(cls, file: pathlib.Path) -> Config:
        return cls._from_dict(yaml.safe_load(file.read_text(encoding="utf-8")))
