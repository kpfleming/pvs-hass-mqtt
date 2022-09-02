from __future__ import annotations

from pytest_mock import MockerFixture

import hass_mqtt.mqtt
from hass_mqtt import MQTT


def test_on_connect(mocker: MockerFixture) -> None:
    """Ensure that the on_connect callback forwards to the MQTT object,
    and passes along the 'flags' and 'rc' arguments."""
    mock_func = mocker.patch.object(MQTT, "_on_connect", autospec=True)
    mqtt = MQTT(broker="", port=0, keep_alive=0, qos=0, discovery_prefix="")
    hass_mqtt.mqtt._on_connect(None, mqtt, {"flag": 42}, -42)
    mock_func.assert_called_once_with(mqtt, {"flag": 42}, -42)


def test_on_discconnect(mocker: MockerFixture) -> None:
    """Ensure that the on_disconnect callback forwards to the MQTT object,
    and passes along the 'rc' argument."""
    mock_func = mocker.patch.object(MQTT, "_on_disconnect", autospec=True)
    mqtt = MQTT(broker="", port=0, keep_alive=0, qos=0, discovery_prefix="")
    hass_mqtt.mqtt._on_disconnect(None, mqtt, -42)
    mock_func.assert_called_once_with(mqtt, -42)
