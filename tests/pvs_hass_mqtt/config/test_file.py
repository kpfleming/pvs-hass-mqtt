from __future__ import annotations

import pathlib

import cerberus  # type: ignore
import pytest
import yaml
from attrs import define

from pvs_hass_mqtt.config import Config, ConfigValidationError


@define(kw_only=True)
class MinimalConfig:
    config_file: pathlib.Path
    data_dir: pathlib.Path
    args: list[str]


@pytest.fixture()
def minimal_config(tmp_path: pathlib.Path) -> MinimalConfig:
    """
    Create a MinimalConfig object which contains a path to an empty
    configuration file and a path to a writable data directory.
    """
    config_file = tmp_path / "config.yml"
    config_file.write_text("")
    return MinimalConfig(
        config_file=config_file,
        data_dir=tmp_path,
        args=["--config-file", str(config_file), "--data-dir", str(tmp_path)],
    )


class TestConfigFile:
    def test_minimal(self, minimal_config: MinimalConfig) -> None:
        """Ensure that a minimal configuration file is accepted."""
        minimal_config.config_file.write_text(
            yaml.dump({"pvs": {"first": {"url": "foo"}}, "array": {"a": {"panel": ["abc"]}}})
        )
        Config.from_file(minimal_config.config_file)

    def test_bad_yaml(self, minimal_config: MinimalConfig) -> None:
        """Ensure that bad YAML in a configuration file is not accepted."""
        minimal_config.config_file.write_text(
            """
            pvs:
              first;
                url: foo
            array:
              a:
                panel:
                  - abc
            """
        )
        with pytest.raises(yaml.scanner.ScannerError):
            Config.from_file(minimal_config.config_file)

    def test_non_yaml(self, minimal_config: MinimalConfig) -> None:
        """Ensure that a configuration file containing non-YAML is not accepted."""
        minimal_config.config_file.write_text(
            """
            The quick brown fox jumps over the lazy dog.
            """
        )
        with pytest.raises(cerberus.validator.DocumentError):
            Config.from_file(minimal_config.config_file)

    def test_file_path_in_error_message(self, minimal_config: MinimalConfig) -> None:
        """Ensure that the path to an invalid configuration file is included in the error message."""
        minimal_config.config_file.write_text(yaml.dump({"pvs": {"first": {"url": "foo"}}}))
        with pytest.raises(ConfigValidationError) as excinfo:
            Config.from_file(minimal_config.config_file)

        assert excinfo.value.message.startswith(str(minimal_config.config_file))
