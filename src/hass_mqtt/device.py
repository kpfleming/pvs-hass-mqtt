from __future__ import annotations

import logging

from attrs import define

logger = logging.getLogger(__name__)


class DeviceConfigurationException(Exception):
    pass


@define(kw_only=True)
class Device:
    configuration_url: str | None
    connections: list[tuple[str, str]] | None
    hw_version: str | None
    identifiers: str | list[str] | None
    manufacturer: str | None
    model: str | None
    name: str | None
    suggested_area: str | None
    sw_version: str | None
    via_device: str | None

    def __attrs_post_init__(self) -> None:
        if not self.connections and not self.identifiers:
            raise DeviceConfigurationException(
                "Either 'connections' or 'identifiers' must be configured."
            )
