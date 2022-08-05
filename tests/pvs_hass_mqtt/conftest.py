from __future__ import annotations

import importlib
import logging
from collections.abc import Iterator
from types import ModuleType

import pytest


@pytest.fixture()
def resettable_logging() -> Iterator[ModuleType]:
    yield logging
    logging.shutdown()
    importlib.reload(logging)
