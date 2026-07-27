"""Core enumerations used throughout Sensora."""

from enum import Enum


class BusType(str, Enum):
    """Supported hardware communication buses."""

    I2C = "i2c"
    SPI = "spi"
    UART = "uart"
    USB = "usb"
    GPIO = "gpio"
    ONEWIRE = "onewire"


class DeviceStatus(str, Enum):
    """Current state of a discovered device."""

    DETECTED = "detected"
    UNKNOWN = "unknown"
    OFFLINE = "offline"
    ERROR = "error"
