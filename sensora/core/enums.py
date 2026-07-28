"""
Core enumerations used throughout Sensora.
"""

from enum import Enum


class BusType(str, Enum):
    """
    Supported hardware communication buses.
    """

    I2C = "i2c"
    I3C = "i3c"

    SPI = "spi"

    UART = "uart"
    RS232 = "rs232"
    RS485 = "rs485"

    USB = "usb"

    CAN = "can"
    LIN = "lin"

    GPIO = "gpio"

    ONEWIRE = "onewire"

    ETHERNET = "ethernet"


class DeviceStatus(str, Enum):
    """
    Current state of a discovered device.
    """

    DETECTED = "detected"

    IDENTIFIED = "identified"

    UNKNOWN = "unknown"

    ONLINE = "online"

    OFFLINE = "offline"

    ERROR = "error"
