from __future__ import annotations

from types import ModuleType

import pytest


@pytest.fixture(autouse=True)
def auto_resettable_logging(resettable_logging: ModuleType) -> ModuleType:
    return resettable_logging
