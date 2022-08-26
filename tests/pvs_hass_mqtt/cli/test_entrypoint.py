from __future__ import annotations

import json
import logging
import pathlib
from types import ModuleType

import pytest
from attrs import define
from pytest_mock import MockerFixture

from pvs_hass_mqtt.cli import cli


@define(kw_only=True)
class MinimalConfig:
    config_file: pathlib.Path
    data_dir: pathlib.Path
    args: list[str]


@pytest.fixture()
def minimal_config(tmp_path: pathlib.Path) -> MinimalConfig:
    """
    Create a MinimalConfig object which contains a path to a minimal
    configuration file and a path to a writable data directory.
    """
    config_file = tmp_path / "config.yml"
    config_file.write_text(
        json.dumps(
            {
                "pvs": {"first": {"url": "foo"}},
                "array": {"a": {"panel": ["1"]}},
                "mqtt": {"broker": "baz"},
            }
        )
    )
    return MinimalConfig(
        config_file=config_file,
        data_dir=tmp_path,
        args=["--config-file", str(config_file), "--data-dir", str(tmp_path)],
    )


@pytest.mark.logging()
@pytest.mark.parametrize(
    ("args", "loglevel"),
    [
        (["--verbose", "--verbose"], logging.DEBUG),
        (["--verbose"], logging.INFO),
        ([], logging.WARNING),
    ],
)
def test_verbose_to_loglevel(
    args: list[str], loglevel: int, resettable_logging: ModuleType, minimal_config: MinimalConfig
) -> None:
    """Ensure that '--verbose' arguments are properly mapped to logging levels."""
    cli(minimal_config.args + args, test_only=True)
    assert logging.root.getEffectiveLevel() == loglevel


@pytest.mark.logging()
def test_systemd_logging_not_possible(mocker: MockerFixture, minimal_config: MinimalConfig) -> None:
    """Ensure that asking for systemd-based logging fails when it is not available."""
    mocker.patch.dict("os.environ", clear=True)
    with pytest.raises(SystemExit) as excinfo:
        cli(
            minimal_config.args + ["--log", "systemd"],
            test_only=True,
        )
    assert excinfo.value.code == 2


@pytest.mark.logging()
def test_missing_config_file(resettable_logging: ModuleType, minimal_config: MinimalConfig) -> None:
    """Ensure that a missing configuration file causes the entrypoint to exit."""
    with pytest.raises(SystemExit) as excinfo:
        cli(
            [
                "--config-file",
                str(minimal_config.config_file) + ".doesnotexist",
                "--data-dir",
                str(minimal_config.data_dir),
            ],
            test_only=True,
        )
    assert excinfo.value.code == 3


@pytest.mark.logging()
def test_missing_data_dir(resettable_logging: ModuleType, minimal_config: MinimalConfig) -> None:
    """Ensure that a missing data directory causes the entrypoint to exit."""
    with pytest.raises(SystemExit) as excinfo:
        cli(
            [
                "--config-file",
                str(minimal_config.config_file),
                "--data-dir",
                str(minimal_config.data_dir) + ".doesnotexist",
            ],
            test_only=True,
        )
    assert excinfo.value.code == 4


@pytest.mark.logging()
def test_config_invalid(resettable_logging: ModuleType, minimal_config: MinimalConfig) -> None:
    """Ensure that invalid config in a configuration file causes the entrypoint to exit."""
    minimal_config.config_file.write_text(
        """
        pvs:
          first:
            url: foo
        array:
          a:
            panel:
              - abc
              - abc
        """
    )
    with pytest.raises(SystemExit) as excinfo:
        cli(minimal_config.args, test_only=True)
    assert excinfo.value.code == 5


@pytest.mark.logging()
def test_config_file_bad_yaml(
    resettable_logging: ModuleType, minimal_config: MinimalConfig
) -> None:
    """Ensure that bad YAML in a configuration file causes the entrypoint to exit."""
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
    with pytest.raises(SystemExit) as excinfo:
        cli(minimal_config.args, test_only=True)
    assert excinfo.value.code == 6


@pytest.mark.logging()
def test_config_file_non_yaml(
    resettable_logging: ModuleType, minimal_config: MinimalConfig
) -> None:
    """Ensure that non-YAML in a configuration file causes the entrypoint to exit."""
    minimal_config.config_file.write_text(
        """
        The quick brown fox jumps over the lazy dog.
        """
    )
    with pytest.raises(SystemExit) as excinfo:
        cli(minimal_config.args, test_only=True)
    assert excinfo.value.code == 6
