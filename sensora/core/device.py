"""Core device model used throughout Sensora."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from sensora.core.enums import BusType, DeviceStatus


@dataclass(slots=True)
class Device:
    """
    Represents a single hardware device discovered by Sensora.

    Every scanner returns one or more Device objects which are then
    consumed by diagnostics, reports, plugins, and the CLI.
    """

    name: str
    bus: BusType

    manufacturer: str | None = None
    address: int | None = None
    chip_id: int | None = None

    status: DeviceStatus = DeviceStatus.UNKNOWN

    description: str | None = None

    metadata: dict[str, Any] | None = None
