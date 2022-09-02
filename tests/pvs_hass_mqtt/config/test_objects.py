from __future__ import annotations

import pytest

from pvs_hass_mqtt.config import Config, ConfigValidationError


def test_simple() -> None:
    """Ensure that the objects from a simple configuration appear in the result."""
    config = Config._from_dict(
        {
            "pvs": {"first": {"url": "foo"}},
            "array": {"a": {"panel": ["abc"]}},
            "mqtt": {"broker": "baz"},
        }
    )
    assert len(config.pvs) == 1
    pvs = config.pvs[0]
    assert pvs.name == "first"
    assert pvs.url == "foo"
    assert len(config.array) == 1
    array = config.array[0]
    assert array.name == "a"
    assert len(array.panel) == 1
    assert array.panel[0].serial == "abc"


class TestPVS:
    def test_multiple(self) -> None:
        """Ensure that multiple PVS appear in the result."""
        config = Config._from_dict(
            {
                "pvs": {"first": {"url": "foo"}, "second": {"url": "bar"}},
                "array": {"a": {"panel": ["abc"]}},
                "mqtt": {"broker": "baz"},
            }
        )
        assert len(config.pvs) == 2
        assert config.pvs[0].name == "first"
        assert config.pvs[1].name == "second"

    def test_default_poll_interval(self) -> None:
        """Ensure that the default poll interval appears in the result."""
        config = Config._from_dict(
            {
                "pvs": {"first": {"url": "foo"}},
                "array": {"a": {"panel": ["abc"]}},
                "mqtt": {"broker": "baz"},
            }
        )
        assert config.pvs[0].poll_interval == 60

    def test_poll_interval(self) -> None:
        """Ensure that the specified poll interval appears in the result."""
        config = Config._from_dict(
            {
                "pvs": {"first": {"url": "foo", "poll_interval": 53}},
                "array": {"a": {"panel": ["abc"]}},
                "mqtt": {"broker": "baz"},
            }
        )
        assert config.pvs[0].poll_interval == 53


class TestArray:
    def test_multiple(self) -> None:
        """Ensure that multiple Array appear in the result."""
        config = Config._from_dict(
            {
                "pvs": {"first": {"url": "foo"}},
                "array": {"a": {"panel": ["abc"]}, "b": {"panel": ["def"]}},
                "mqtt": {"broker": "baz"},
            }
        )
        assert len(config.array) == 2
        assert config.array[0].name == "a"
        assert config.array[1].name == "b"

    def test_details(self) -> None:
        """Ensure that the details for an Array appear in the result."""
        config = Config._from_dict(
            {
                "pvs": {"first": {"url": "foo"}},
                "array": {"a": {"azimuth": 123.4, "tilt": 76.8, "panel": ["abc"]}},
                "mqtt": {"broker": "baz"},
            }
        )
        assert config.array[0].azimuth == 123.4
        assert config.array[0].tilt == 76.8


class TestPanel:
    def test_duplicate_serial(self) -> None:
        """Ensure that two Panels with the same serial are not accepted."""
        with pytest.raises(ConfigValidationError) as excinfo:
            Config._from_dict(
                {
                    "pvs": {"first": {"url": "foo"}},
                    "array": {"a": {"panel": ["abc", "abc"]}},
                    "mqtt": {"broker": "baz"},
                }
            )

        assert excinfo.value.message == "Panel 'abc' defined more than once"

    def test_same_serial_multiple_arrays(self) -> None:
        """Ensure that two Panels with the same serial, in different Arrays, are not accepted."""
        with pytest.raises(ConfigValidationError) as excinfo:
            Config._from_dict(
                {
                    "pvs": {"first": {"url": "foo"}},
                    "array": {"a": {"panel": ["abc"]}, "b": {"panel": ["abc"]}},
                    "mqtt": {"broker": "baz"},
                }
            )

        assert excinfo.value.message == "Panel 'abc' defined more than once"


class TestMQTT:
    def test_broker(self) -> None:
        """Ensure that the specified broker appears in the result."""
        config = Config._from_dict(
            {
                "pvs": {"first": {"url": "foo"}},
                "array": {"a": {"panel": ["abc"]}},
                "mqtt": {"broker": "baz"},
            }
        )
        assert config.mqtt.broker == "baz"

    def test_default_port(self) -> None:
        """Ensure that the default port number appears in the result."""
        config = Config._from_dict(
            {
                "pvs": {"first": {"url": "foo"}},
                "array": {"a": {"panel": ["abc"]}},
                "mqtt": {"broker": "baz"},
            }
        )
        assert config.mqtt.port == 1883

    def test_port(self) -> None:
        """Ensure that the specified port number appears in the result."""
        config = Config._from_dict(
            {
                "pvs": {"first": {"url": "foo"}},
                "array": {"a": {"panel": ["abc"]}},
                "mqtt": {"broker": "baz", "port": 1337},
            }
        )
        assert config.mqtt.port == 1337

    def test_username(self) -> None:
        """Ensure that the specified username appears in the result."""
        config = Config._from_dict(
            {
                "pvs": {"first": {"url": "foo"}},
                "array": {"a": {"panel": ["abc"]}},
                "mqtt": {"broker": "baz", "username": "flibber"},
            }
        )
        assert config.mqtt.username == "flibber"

    def test_password(self) -> None:
        """Ensure that the specified password appears in the result."""
        config = Config._from_dict(
            {
                "pvs": {"first": {"url": "foo"}},
                "array": {"a": {"panel": ["abc"]}},
                "mqtt": {"broker": "baz", "password": "flibber"},
            }
        )
        assert config.mqtt.password == "flibber"

    def test_client_id(self) -> None:
        """Ensure that the specified client_id appears in the result."""
        config = Config._from_dict(
            {
                "pvs": {"first": {"url": "foo"}},
                "array": {"a": {"panel": ["abc"]}},
                "mqtt": {"broker": "baz", "client_id": "flibber"},
            }
        )
        assert config.mqtt.client_id == "flibber"

    def test_default_keep_alive(self) -> None:
        """Ensure that the default keep_alive appears in the result."""
        config = Config._from_dict(
            {
                "pvs": {"first": {"url": "foo"}},
                "array": {"a": {"panel": ["abc"]}},
                "mqtt": {"broker": "baz"},
            }
        )
        assert config.mqtt.keep_alive == 30

    def test_keep_alive(self) -> None:
        """Ensure that the specified keep_alive appears in the result."""
        config = Config._from_dict(
            {
                "pvs": {"first": {"url": "foo"}},
                "array": {"a": {"panel": ["abc"]}},
                "mqtt": {"broker": "baz", "keep_alive": 90},
            }
        )
        assert config.mqtt.keep_alive == 90

    def test_default_qos(self) -> None:
        """Ensure that the default qos appears in the result."""
        config = Config._from_dict(
            {
                "pvs": {"first": {"url": "foo"}},
                "array": {"a": {"panel": ["abc"]}},
                "mqtt": {"broker": "baz"},
            }
        )
        assert config.mqtt.qos == 0

    def test_qos(self) -> None:
        """Ensure that the specified qos appears in the result."""
        config = Config._from_dict(
            {
                "pvs": {"first": {"url": "foo"}},
                "array": {"a": {"panel": ["abc"]}},
                "mqtt": {"broker": "baz", "qos": 2},
            }
        )
        assert config.mqtt.qos == 2

    def test_default_discovery_prefix(self) -> None:
        """Ensure that the default discovery_prefix appears in the result."""
        config = Config._from_dict(
            {
                "pvs": {"first": {"url": "foo"}},
                "array": {"a": {"panel": ["abc"]}},
                "mqtt": {"broker": "baz"},
            }
        )
        assert config.mqtt.discovery_prefix == "homeassistant"

    def test_discovery_prefix(self) -> None:
        """Ensure that the specified discovery_prefix appears in the result."""
        config = Config._from_dict(
            {
                "pvs": {"first": {"url": "foo"}},
                "array": {"a": {"panel": ["abc"]}},
                "mqtt": {"broker": "baz", "discovery_prefix": "blah"},
            }
        )
        assert config.mqtt.discovery_prefix == "blah"
