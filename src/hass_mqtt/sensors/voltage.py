from __future__ import annotations

import logging

from attrs import define

from ..sensor import Sensor, SensorDeviceClass, SensorStateClass, UnitOfMeasurement

logger = logging.getLogger(__name__)


@define(kw_only=True)
class VoltageSensor(Sensor):
    def __attrs_post_init__(self) -> None:
        self.device_class = SensorDeviceClass.voltage
        if not self.state_class:
            self.state_class = SensorStateClass.measurement
        if not self.unit_of_measurement:
            self.unit_of_measurement = UnitOfMeasurement.voltage_volt
