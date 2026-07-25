"""Common result object used throughout Sensora."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from sensora.core.device import Device


@dataclass(slots=True)
class Result:
    """
    Represents the outcome of an operation.

    Used by scanners, diagnostics, plugins, and commands to
    return a consistent response.
    """

    success: bool
    message: str = ""

    devices: list[Device] = field(default_factory=list)

    data: dict[str, Any] = field(default_factory=dict)

    error: Exception | None = None
