from __future__ import annotations

from sensora.buses.backend import BusType, get_backend

Backend = get_backend(BusType.ONEWIRE)


class OneWireBus(Backend):
    """Platform-independent OneWire bus."""
