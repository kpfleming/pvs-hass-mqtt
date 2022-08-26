from __future__ import annotations

import logging

from attrs import define, field

from .panel import Panel

logger = logging.getLogger(__name__)


@define(kw_only=True)
class Array:
    name: str
    azimuth: float | None
    tilt: float | None
    panel: list[Panel] = field(factory=list)
