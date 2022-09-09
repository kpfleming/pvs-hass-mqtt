from __future__ import annotations

import logging

from attrs import define

from ..binary_sensor import BinarySensor, BinarySensorDeviceClass

logger = logging.getLogger(__name__)


@define(kw_only=True)
class RunningBinarySensor(BinarySensor):
    def __attrs_post_init__(self) -> None:
        self.device_class = BinarySensorDeviceClass.running
