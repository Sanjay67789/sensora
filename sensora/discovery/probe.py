"""
I²C device probing utilities.
"""

from __future__ import annotations

from sensora.buses.exceptions import DeviceCommunicationError
from sensora.buses.i2c import I2CBus


class I2CProbe:
    """
    Probe I²C addresses for responding devices.

    This class is responsible only for determining whether a
    device exists at a given address. It does not identify
    the device or load any drivers.
    """

    def __init__(self, bus: I2CBus) -> None:
        self._bus = bus

    def exists(self, address: int) -> bool:
        """
        Check whether an I²C device responds at the given address.

        Args:
            address: 7-bit I²C device address.

        Returns:
            True if a device responds, otherwise False.
        """

        try:
            self._bus.read_byte(address)
            return True

        except DeviceCommunicationError:
            return False
