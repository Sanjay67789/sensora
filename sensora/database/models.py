"""
Database models for Sensora hardware definitions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True, frozen=True)
class VendorDefinition:
    """
    Represents a hardware manufacturer.
    """

    id: str
    name: str

    description: str = ""

    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True, frozen=True)
class DeviceDefinition:
    """
    Represents a supported hardware device.
    """

    # Unique device identifier.
    id: str

    # Human-readable device name.
    name: str

    # Vendor identifier.
    vendor: str

    # Human-readable description.
    description: str = ""

    # Supported interfaces.
    interfaces: dict[str, Any] = field(default_factory=dict)

    # Device identification information.
    identification: dict[str, Any] = field(default_factory=dict)

    # Driver information.
    driver: dict[str, Any] = field(default_factory=dict)

    # Linux-specific metadata.
    linux: dict[str, Any] = field(default_factory=dict)

    # Supported measurements.
    measurements: list[str] = field(default_factory=list)

    # Electrical characteristics.
    electrical: dict[str, Any] = field(default_factory=dict)

    # Physical package information.
    package: dict[str, Any] = field(default_factory=dict)

    # Device capabilities.
    features: dict[str, bool] = field(default_factory=dict)

    # Optional metadata.
    metadata: dict[str, Any] = field(default_factory=dict)
