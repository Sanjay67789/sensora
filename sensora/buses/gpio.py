from __future__ import annotations

from sensora.buses.backend import BusType, get_backend

Backend = get_backend(BusType.GPIO)


class GPIOBus(Backend):
    """Platform-independent GPIO bus."""
