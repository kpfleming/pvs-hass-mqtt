from __future__ import annotations

import logging
from collections.abc import Mapping

import paho.mqtt.client as mqtt_client  # type: ignore
from attrs import define, field

logger = logging.getLogger(__name__)


def _on_connect(
    client: mqtt_client.Client, userdata: MQTT, flags: Mapping[str, int], rc: int
) -> None:
    userdata._on_connect(flags, rc)


def _on_disconnect(client: mqtt_client.Client, userdata: MQTT, rc: int) -> None:
    userdata._on_disconnect(rc)


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
    _client: mqtt_client.Client = field(init=False)

    def connect(self) -> None:
        client = mqtt_client.Client(client_id=self.client_id, userdata=self)
        client.enable_logger()
        client.on_connect = _on_connect
        client.on_disconnect = _on_disconnect
        if self.username:
            client.username_pw_set(self.username, self.password)
        client.connect(host=self.broker, port=self.port, keepalive=self.keep_alive)
        self._client = client

    def _on_connect(self, flags: Mapping[str, int], rc: int) -> None:
        pass

    def _on_disconnect(self, rc: int) -> None:
        pass
