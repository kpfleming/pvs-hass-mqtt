from __future__ import annotations

from typing import Any

import pytest

from pvs_hass_mqtt.config import Config, ConfigValidationError


def test_minimal_config() -> None:
    """Ensure that a minimal configuration is accepted."""
    Config._from_dict({"pvs": {"first": {"url": "foo"}}, "array": {"a": {"panel": ["1"]}}})


class TestPVS:
    def test_missing(self) -> None:
        """Ensure that a configuration missing the 'pvs' mapping is not accepted."""
        with pytest.raises(ConfigValidationError) as excinfo:
            Config._from_dict({"array": {"a": {"panel": ["1"]}}})

        errors = excinfo.value.errors
        assert errors is not None
        assert "pvs" in errors
        assert "required field" in errors["pvs"]

    def test_empty(self) -> None:
        """Ensure that a configuration with an empty 'pvs' mapping is not accepted."""
        with pytest.raises(ConfigValidationError) as excinfo:
            Config._from_dict({"pvs": {}, "array": {"a": {"panel": ["1"]}}})

        errors = excinfo.value.errors
        assert errors is not None
        assert "pvs" in errors
        assert "min length is 1" in errors["pvs"]

    @pytest.mark.parametrize(
        "key",
        [
            1,
            1.2,
            False,
        ],
    )
    def test_invalid_key(self, key: Any) -> None:
        """Ensure that an invalid key in the 'pvs' mapping is not accepted."""
        with pytest.raises(ConfigValidationError) as excinfo:
            Config._from_dict({"pvs": {key: {"url": "foo"}}, "array": {"a": {"panel": ["1"]}}})

        errors = excinfo.value.errors
        assert errors is not None
        assert "pvs" in errors
        assert key in errors["pvs"][0]
        assert "must be of string type" in errors["pvs"][0][key]

    def test_missing_url(self) -> None:
        """Ensure that a missing 'url' field in a 'pvs' mapping entry is not accepted."""
        with pytest.raises(ConfigValidationError) as excinfo:
            Config._from_dict(
                {"pvs": {"first": {"poll_interval": 60}}, "array": {"a": {"panel": ["1"]}}}
            )

        errors = excinfo.value.errors
        assert errors is not None
        assert "pvs" in errors
        assert "url" in errors["pvs"][0]["first"][0]
        assert "required field" in errors["pvs"][0]["first"][0]["url"]

    @pytest.mark.parametrize(
        ("value", "error"),
        [
            (15, "min value"),
            (1.2, "integer type"),
            ("abc", "integer type"),
        ],
    )
    def test_invalid_poll_interval(self, value: Any, error: str) -> None:
        """Ensure that invalid values for the 'poll_interval' field in a 'pvs' mapping entry are not accepted."""
        with pytest.raises(ConfigValidationError) as excinfo:
            Config._from_dict(
                {
                    "pvs": {"first": {"url": "foo", "poll_interval": value}},
                    "array": {"a": {"panel": ["1"]}},
                }
            )

        errors = excinfo.value.errors
        assert errors is not None
        assert "pvs" in errors
        assert "poll_interval" in errors["pvs"][0]["first"][0]
        assert error in errors["pvs"][0]["first"][0]["poll_interval"][0]

    def test_multiple(self) -> None:
        """Ensure that the 'pvs' mapping can contain multiple objects."""
        Config._from_dict(
            {
                "pvs": {"first": {"url": "foo"}, "second": {"url": "foo"}},
                "array": {"a": {"panel": ["1"]}},
            }
        )


class TestArray:
    def test_missing(self) -> None:
        """Ensure that a configuration missing the 'array' mapping is not accepted."""
        with pytest.raises(ConfigValidationError) as excinfo:
            Config._from_dict({"pvs": {"first": {"url": "foo"}}})

        errors = excinfo.value.errors
        assert errors is not None
        assert "array" in errors
        assert "required field" in errors["array"]

    def test_empty(self) -> None:
        """Ensure that a configuration with an empty 'array' mapping is not accepted."""
        with pytest.raises(ConfigValidationError) as excinfo:
            Config._from_dict({"pvs": {"first": {"url": "foo"}}, "array": {}})

        errors = excinfo.value.errors
        assert errors is not None
        assert "array" in errors
        assert "min length is 1" in errors["array"]

    @pytest.mark.parametrize(
        "key",
        [
            1,
            1.2,
            False,
        ],
    )
    def test_invalid_key(self, key: Any) -> None:
        """Ensure that an invalid key in the 'array' mapping is not accepted."""
        with pytest.raises(ConfigValidationError) as excinfo:
            Config._from_dict({"pvs": {"first": {"url": "foo"}}, "array": {key: {"panel": ["1"]}}})

        errors = excinfo.value.errors
        assert errors is not None
        assert "array" in errors
        assert key in errors["array"][0]
        assert "must be of string type" in errors["array"][0][key]

    def test_missing_panel(self) -> None:
        """Ensure that a missing 'panel' list in a 'array' mapping entry is not accepted."""
        with pytest.raises(ConfigValidationError) as excinfo:
            Config._from_dict({"pvs": {"first": {"poll_interval": 60}}, "array": {"a": {}}})

        errors = excinfo.value.errors
        assert errors is not None
        assert "array" in errors
        assert "panel" in errors["array"][0]["a"][0]
        assert "required field" in errors["array"][0]["a"][0]["panel"]

    def test_multiple(self) -> None:
        """Ensure that the 'array' mapping can contain multiple objects."""
        Config._from_dict(
            {
                "pvs": {"first": {"url": "foo"}, "second": {"url": "foo"}},
                "array": {"a": {"panel": ["1"]}, "b": {"panel": ["2"]}},
            }
        )

    @pytest.mark.parametrize(
        "panel",
        [
            1,
            1.2,
            False,
        ],
    )
    def test_invalid_panel(self, panel: Any) -> None:
        """Ensure that an invalid serial number in the 'panel' list is not accepted."""
        with pytest.raises(ConfigValidationError) as excinfo:
            Config._from_dict(
                {"pvs": {"first": {"url": "foo"}}, "array": {"a": {"panel": [panel]}}}
            )

        errors = excinfo.value.errors
        assert errors is not None
        assert "array" in errors
        assert "panel" in errors["array"][0]["a"][0]
        assert "must be of string type" in errors["array"][0]["a"][0]["panel"][0][0]

    def test_azimuth(self) -> None:
        """Ensure that an 'azimuth' field in an entry in the 'array' mapping is accepted."""
        Config._from_dict(
            {
                "pvs": {"first": {"url": "foo"}, "second": {"url": "foo"}},
                "array": {"a": {"panel": ["1"], "azimuth": 123.45}},
            }
        )

    @pytest.mark.parametrize(
        ("value", "error"),
        [
            (-1.0, "min value"),
            (361.0, "max value"),
            ("abc", "float type"),
        ],
    )
    def test_invalid_azimuth(self, value: Any, error: str) -> None:
        """Ensure that invalid 'azimuth' values in an entry in the 'array' mapping are not accepted."""
        with pytest.raises(ConfigValidationError) as excinfo:
            Config._from_dict(
                {
                    "pvs": {"first": {"url": "foo"}, "second": {"url": "foo"}},
                    "array": {"a": {"panel": ["1"], "azimuth": value}},
                }
            )

        errors = excinfo.value.errors
        assert errors is not None
        assert "array" in errors
        assert "azimuth" in errors["array"][0]["a"][0]
        assert error in errors["array"][0]["a"][0]["azimuth"][0]

    def test_tilt(self) -> None:
        """Ensure that a 'tilt' field in an entry in the 'array' mapping is accepted."""
        Config._from_dict(
            {
                "pvs": {"first": {"url": "foo"}, "second": {"url": "foo"}},
                "array": {"a": {"panel": ["1"], "tilt": 12.34}},
            }
        )

    @pytest.mark.parametrize(
        ("value", "error"),
        [
            (-1.0, "min value"),
            (91.0, "max value"),
            ("abc", "float type"),
        ],
    )
    def test_invalid_tilt(self, value: Any, error: str) -> None:
        """Ensure that invalid 'tilt' values in an entry in the 'array' mapping are not accepted."""
        with pytest.raises(ConfigValidationError) as excinfo:
            Config._from_dict(
                {
                    "pvs": {"first": {"url": "foo"}, "second": {"url": "foo"}},
                    "array": {"a": {"panel": ["1"], "tilt": value}},
                }
            )

        errors = excinfo.value.errors
        assert errors is not None
        assert "array" in errors
        assert "tilt" in errors["array"][0]["a"][0]
        assert error in errors["array"][0]["a"][0]["tilt"][0]
