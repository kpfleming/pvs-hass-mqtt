from __future__ import annotations

import pytest
from mock import MagicMock
from pytest_mock import MockerFixture

from hass_mqtt import MQTT


@pytest.fixture()
def mock_client(mocker: MockerFixture) -> MagicMock:
    """Mock the MQTT client class."""
    mock_class = mocker.patch("hass_mqtt.mqtt.mqtt_client.Client", autospec=True)
    return mock_class


def test_userdata(mock_client: MagicMock) -> None:
    """Ensure that the MQTT object is passed as userdata to the MQTT client."""
    mqtt = MQTT(broker="", port=0, keep_alive=0, qos=0, hass_topic_prefix="")
    mqtt.connect()
    mock_client.assert_called_once()
    assert "userdata" in mock_client.call_args.kwargs
    assert mock_client.call_args.kwargs["userdata"] is mqtt


def test_no_client_id(mock_client: MagicMock) -> None:
    """Ensure that if no client_id is specified then none is passed to the MQTT client."""
    mqtt = MQTT(broker="", port=0, keep_alive=0, qos=0, hass_topic_prefix="")
    mqtt.connect()
    mock_client.assert_called_once()
    assert "client_id" in mock_client.call_args.kwargs
    assert mock_client.call_args.kwargs["client_id"] is None


def test_client_id(mock_client: MagicMock) -> None:
    """Ensure that if a client_id is specified it is passed to the MQTT client."""
    mqtt = MQTT(client_id="baz", broker="", port=0, keep_alive=0, qos=0, hass_topic_prefix="")
    mqtt.connect()
    mock_client.assert_called_once()
    assert "client_id" in mock_client.call_args.kwargs
    assert mock_client.call_args.kwargs["client_id"] == "baz"


def test_logger_enabled(mock_client: MagicMock) -> None:
    """Ensure that logging using the Python logging facility is enabled."""
    MQTT(broker="", port=0, keep_alive=0, qos=0, hass_topic_prefix="").connect()
    mock_client.return_value.enable_logger.assert_called_once()


def test_no_username(mock_client: MagicMock) -> None:
    """Ensure that if no username is specified then none is passed to the MQTT client."""
    MQTT(broker="", port=0, keep_alive=0, qos=0, hass_topic_prefix="").connect()
    mock_client.return_value.username_pw_set.assert_not_called()


def test_username(mock_client: MagicMock) -> None:
    """Ensure that if a username is specified then it is passed to the MQTT client."""
    MQTT(
        broker="", port=0, keep_alive=0, qos=0, hass_topic_prefix="", username="foo", password="bar"
    ).connect()
    mock_client.return_value.username_pw_set.assert_called_once_with("foo", "bar")


def test_broker_port_keep_alive(mock_client: MagicMock) -> None:
    """Ensure that the specified broker, port, and keep_alive are passed to the MQTT client."""
    MQTT(broker="baz", port=42, keep_alive=39, qos=0, hass_topic_prefix="").connect()
    mock_client.return_value.connect.assert_called_once_with(host="baz", port=42, keepalive=39)
