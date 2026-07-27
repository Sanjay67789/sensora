from __future__ import annotations

from sensora.buses.backend import BusType, get_backend

Backend = get_backend(BusType.I2C)


class I2CBus(Backend):
    """Platform-independent I²C bus."""

    pass
