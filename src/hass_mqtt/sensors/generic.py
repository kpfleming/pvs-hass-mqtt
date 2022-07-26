from __future__ import annotations

import logging

from attrs import define

from ..sensor import Sensor

logger = logging.getLogger(__name__)


@define(kw_only=True)
class GenericSensor(Sensor):
    def __attrs_post_init__(self) -> None:
        self.device_class = None
