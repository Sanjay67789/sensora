from __future__ import annotations

from sensora.buses.backend import BusType, get_backend

Backend = get_backend(BusType.UART)


class UARTBus(Backend):
    """Platform-independent UART bus."""
