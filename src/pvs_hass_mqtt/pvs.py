from __future__ import annotations

import logging

from attrs import define

logger = logging.getLogger(__name__)


@define(kw_only=True)
class PVS:
    name: str
    url: str
    poll_interval: int
