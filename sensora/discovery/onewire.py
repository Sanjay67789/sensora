"""
1-Wire device scanner.
"""

from __future__ import annotations

from sensora.buses.onewire import OneWireBus
from sensora.core.device import Device
from sensora.core.enums import BusType
from sensora.discovery.base import BaseScanner
from sensora.discovery.result import ScanResult


class OneWireScanner(BaseScanner):
    """
    Discover devices on a 1-Wire bus.
    """

    def __init__(
        self,
        bus: OneWireBus,
    ) -> None:
        self._bus = bus

    def scan(self) -> ScanResult:
        """
        Scan the 1-Wire bus.

        Returns
        -------
        ScanResult
            Discovery results.
        """
        result = ScanResult()

        self._bus.open()

        for rom in self._bus.scan():
            result.devices.append(
                Device(
                    name="Unknown 1-Wire Device",
                    bus=BusType.ONEWIRE,
                    metadata={
                        "rom": rom,
                    },
                )
            )

        return result
