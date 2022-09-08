from __future__ import annotations

import logging
from enum import Enum, auto
from typing import Protocol

from attrs import define, field

from . import Entity

logger = logging.getLogger(__name__)


class SensorDeviceClass(Enum):
    apparent_power = auto()
    aql = auto()
    battery = auto()
    carbon_dioxide = auto()
    carbon_monoxide = auto()
    current = auto()
    date = auto()
    duration = auto()
    energy = auto()
    frequency = auto()
    gas = auto()
    humidity = auto()
    illuminance = auto()
    monetary = auto()
    nitrogen_dioxide = auto()
    nitrogen_monoxide = auto()
    nitrous_oxide = auto()
    ozone = auto()
    pm1 = auto()
    pm10 = auto()
    pm25 = auto()
    power_factor = auto()
    power = auto()
    pressure = auto()
    reactive_power = auto()
    signal_strength = auto()
    sulphur_dioxide = auto()
    temperature = auto()
    timestamp = auto()
    volatile_organic_compounds = auto()
    voltage = auto()


@define(kw_only=True)
class Sensor(Entity, Protocol):
    # need state_class
    # need unit_of_measurement
    device_class: SensorDeviceClass | None = field(init=False)
