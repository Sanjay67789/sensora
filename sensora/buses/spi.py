from __future__ import annotations

from sensora.buses.backend import BusType, get_backend

Backend = get_backend(BusType.SPI)


class SPIBus(Backend):
    """Platform-independent SPI bus."""
