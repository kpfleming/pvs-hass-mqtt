from __future__ import annotations

import logging
from enum import Enum, auto
from typing import Protocol

from attrs import define, field

from .entity import Entity

logger = logging.getLogger(__name__)


class BinarySensorDeviceClass(Enum):
    battery = auto()
    battery_charging = auto()
    carbon_monoxide = auto()
    cold = auto()
    connectivity = auto()
    door = auto()
    garage_door = auto()
    gas = auto()
    heat = auto()
    light = auto()
    lock = auto()
    moisture = auto()
    motion = auto()
    moving = auto()
    occupancy = auto()
    opening = auto()
    plug = auto()
    power = auto()
    presence = auto()
    problem = auto()
    running = auto()
    safety = auto()
    smoke = auto()
    sound = auto()
    tamper = auto()
    update = auto()
    vibration = auto()
    window = auto()


@define(kw_only=True)
class BinarySensor(Entity, Protocol):
    device_class: BinarySensorDeviceClass | None = field(init=False)
    off_delay: int | None = None
    state: bool = False
