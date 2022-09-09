from __future__ import annotations

import logging

from attrs import define

from ..sensor import Sensor, SensorDeviceClass

logger = logging.getLogger(__name__)


@define(kw_only=True)
class PowerFactorSensor(Sensor):
    def __attrs_post_init__(self) -> None:
        self.device_class = SensorDeviceClass.power_factor
