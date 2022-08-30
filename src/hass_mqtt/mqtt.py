from __future__ import annotations

import logging

from attrs import define

logger = logging.getLogger(__name__)


@define(kw_only=True)
class MQTT:
    broker: str
    port: int
    username: str | None
    password: str | None
    client_id: str | None
    keep_alive: int
    qos: int
    hass_topic_prefix: str
