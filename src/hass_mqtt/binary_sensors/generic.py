from __future__ import annotations

import logging

from attrs import define

from ..binary_sensor import BinarySensor

logger = logging.getLogger(__name__)


@define(kw_only=True)
class GenericBinarySensor(BinarySensor):
    def __attrs_post_init__(self) -> None:
        self.device_class = None
