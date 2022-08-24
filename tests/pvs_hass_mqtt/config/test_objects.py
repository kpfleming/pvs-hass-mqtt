from __future__ import annotations

import pytest

from pvs_hass_mqtt.config import Config, ConfigValidationError


class TestConfig:
    def test_simple(self) -> None:
        """Ensure that the objects from a simple configuration appear in the result."""
        config = Config._from_dict(
            {"pvs": {"first": {"url": "foo"}}, "array": {"a": {"panel": ["abc"]}}}
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

    def test_multiple_pvs(self) -> None:
        """Ensure that multiple PVS appear in the result."""
        config = Config._from_dict(
            {
                "pvs": {"first": {"url": "foo"}, "second": {"url": "bar"}},
                "array": {"a": {"panel": ["abc"]}},
            }
        )
        assert len(config.pvs) == 2
        assert config.pvs[0].name == "first"
        assert config.pvs[1].name == "second"

    def test_multiple_array(self) -> None:
        """Ensure that multiple Array appear in the result."""
        config = Config._from_dict(
            {
                "pvs": {"first": {"url": "foo"}},
                "array": {"a": {"panel": ["abc"]}, "b": {"panel": ["def"]}},
            }
        )
        assert len(config.array) == 2
        assert config.array[0].name == "a"
        assert config.array[1].name == "b"

    def test_duplicate_panel_serial(self) -> None:
        """Ensure that two Panels with the same serial are not accepted."""
        with pytest.raises(ConfigValidationError) as excinfo:
            Config._from_dict(
                {
                    "pvs": {"first": {"url": "foo"}},
                    "array": {"a": {"panel": ["abc", "abc"]}},
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
                }
            )

        assert excinfo.value.message == "Panel 'abc' defined more than once"

    def test_array_details(self) -> None:
        """Ensure that the details for an Array appear in the result."""
        config = Config._from_dict(
            {
                "pvs": {"first": {"url": "foo"}},
                "array": {"a": {"azimuth": 123.4, "tilt": 76.8, "panel": ["abc"]}},
            }
        )
        assert config.array[0].azimuth == 123.4
        assert config.array[0].tilt == 76.8
