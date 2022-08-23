from __future__ import annotations

from pvs_hass_mqtt.config import Config


def test_minimal_config() -> None:
    Config._from_dict({})
