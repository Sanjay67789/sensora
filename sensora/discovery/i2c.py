"""I²C discovery implementation."""

from __future__ import annotations

from sensora.buses.i2c import I2CBus
from sensora.core.result import Result
from sensora.discovery.base import BaseScanner


class I2CScanner(BaseScanner):
    """Discover devices connected to an I²C bus."""

    def __init__(self, bus_id: int = 1) -> None:
        self._bus = I2CBus(bus_id)

    def scan(self) -> Result:
        """
        Scan the I²C bus.

        Implementation will be added after
        I2CBus communication methods are complete.
        """
        raise NotImplementedError
