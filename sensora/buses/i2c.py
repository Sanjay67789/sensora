"""I²C bus implementation for Sensora."""

from __future__ import annotations

from smbus2 import SMBus

from sensora.buses.base import BaseBus
from sensora.core.result import Result


class I2CBus(BaseBus):
    """Implementation of the Linux I²C communication bus."""

    def __init__(self, bus_id: int = 1) -> None:
        self._bus_id = bus_id
        self._bus: SMBus | None = None

    def open(self) -> None:
        """Open the I²C bus."""
        if self._bus is None:
            self._bus = SMBus(self._bus_id)

    def close(self) -> None:
        """Close the I²C bus."""
        if self._bus is not None:
            self._bus.close()
            self._bus = None

    @property
    def is_open(self) -> bool:
        """Return True if the I²C bus is open."""
        return self._bus is not None

    @property
    def bus_id(self) -> int:
        """Linux I²C bus number."""
        return self._bus_id

    def scan(self) -> Result:
        raise NotImplementedError

    def read_byte(self, address: int) -> int:
        raise NotImplementedError

    def write_byte(self, address: int, value: int) -> None:
        raise NotImplementedError
