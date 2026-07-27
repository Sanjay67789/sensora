"""
Database models for Sensora hardware definitions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from sensora.core.enums import BusType


@dataclass(slots=True, frozen=True)
class VendorDefinition:
    """
    Represents a hardware manufacturer.
    """

    vendor_id: str
    name: str

    website: str = ""
    country: str = ""

    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True, frozen=True)
class DeviceDefinition:
    """
    Represents a supported hardware device.
    """

    # Stable unique identifier.
    # Example: "bosch.bme280"
    device_id: str

    # Human-readable name.
    # Example: "BME280"
    name: str

    # Vendor identifier.
    # Example: "bosch"
    vendor: str

    # Supported communication buses.
    buses: tuple[BusType, ...]

    # Valid device addresses (if applicable).
    addresses: tuple[int, ...] = ()

    # Optional identification register value.
    chip_id: int | None = None

    # Python module implementing the driver.
    # Example: "bosch.bme280"
    driver_module: str | None = None

    # Human-readable description.
    description: str = ""

    # Additional device information.
    metadata: dict[str, Any] = field(default_factory=dict)
