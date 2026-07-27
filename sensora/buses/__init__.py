"""
Hardware communication buses for Sensora.

This package exposes platform-independent communication bus APIs.

Applications should import buses from this package rather than using
platform-specific implementations directly.
"""

from __future__ import annotations

from sensora.buses.base import BaseBus
from sensora.buses.discovery import ScannableBus
from sensora.buses.exceptions import (
    BusAlreadyOpenError,
    BusError,
    BusNotOpenError,
    BusScanError,
    DeviceCommunicationError,
    InvalidAddressError,
    InvalidDataError,
    InvalidRegisterError,
)
from sensora.buses.gpio import GPIOBus
from sensora.buses.i2c import I2CBus
from sensora.buses.onewire import OneWireBus
from sensora.buses.spi import SPIBus
from sensora.buses.uart import UARTBus

__all__ = [
    # Base interfaces
    "BaseBus",
    "ScannableBus",
    # Public buses
    "I2CBus",
    "SPIBus",
    "UARTBus",
    "GPIOBus",
    "OneWireBus",
    # Exceptions
    "BusError",
    "BusNotOpenError",
    "BusAlreadyOpenError",
    "BusScanError",
    "DeviceCommunicationError",
    "InvalidAddressError",
    "InvalidRegisterError",
    "InvalidDataError",
]
