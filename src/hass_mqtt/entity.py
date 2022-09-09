from __future__ import annotations

import logging
from enum import Enum, auto
from typing import Protocol

from attrs import define

from .device import Device

logger = logging.getLogger(__name__)


class EntityCategory(Enum):
    config = auto()
    diagnostic = auto()


@define(kw_only=True)
class Entity(Protocol):
    name: str
    object_id: str | None = None
    device: Device | None = None
    enabled_by_default: bool = True
    entity_category: EntityCategory | None = None
    expire_after: int = 0
    force_update: bool = False
    icon: str | None = None
