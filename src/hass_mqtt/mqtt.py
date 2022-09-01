from __future__ import annotations

import logging

import paho.mqtt.client as mqtt_client  # type: ignore
from attrs import define, field

logger = logging.getLogger(__name__)


@define(kw_only=True)
class MQTT:
    broker: str
    port: int
    username: str | None = None
    password: str | None = None
    client_id: str | None = None
    keep_alive: int
    qos: int
    hass_topic_prefix: str
    client: mqtt_client.Client = field(init=False)

    def connect(self) -> None:
        client = mqtt_client.Client(client_id=self.client_id, userdata=self)
        client.enable_logger()
        if self.username:
            client.username_pw_set(self.username, self.password)
        client.connect(host=self.broker, port=self.port, keepalive=self.keep_alive)
        self.client = client
