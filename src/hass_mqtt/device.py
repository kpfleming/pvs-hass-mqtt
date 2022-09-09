from __future__ import annotations

import logging

from attrs import define

logger = logging.getLogger(__name__)


class DeviceConfigurationException(Exception):
    pass


@define(kw_only=True, eq=False)
class Device:
    configuration_url: str | None = None
    connections: list[tuple[str, str]] | None = None
    hw_version: str | None = None
    identifiers: str | list[str] | None = None
    manufacturer: str | None = None
    model: str | None = None
    name: str
    suggested_area: str | None = None
    sw_version: str | None = None
    via_device: str | None = None

    def __attrs_post_init__(self) -> None:
        if not self.connections and not self.identifiers:
            raise DeviceConfigurationException(
                "Either 'connections' or 'identifiers' must be configured."
            )
