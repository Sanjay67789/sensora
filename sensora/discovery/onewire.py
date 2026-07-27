"""
1-Wire device scanner.
"""

from __future__ import annotations

from sensora.buses.onewire import OneWireBus
from sensora.core.device import Device
from sensora.core.enums import BusType, DeviceStatus
from sensora.core.result import Result
from sensora.discovery.base import BaseScanner


class OneWireScanner(BaseScanner):
    """
    Discover devices on a 1-Wire bus.
    """

    @property
    def name(self) -> str:
        """
        Human-readable scanner name.
        """
        return "1-Wire"

    def __init__(
        self,
        bus: OneWireBus,
    ) -> None:
        self._bus = bus

    def scan(self) -> Result:
        """
        Scan the 1-Wire bus.

        Returns
        -------
        Result
            Discovery results.
        """

        devices: list[Device] = []

        try:
            self._bus.open()

            for rom in self._bus.scan():
                devices.append(
                    Device(
                        name="Unknown 1-Wire Device",
                        bus=BusType.ONEWIRE,
                        status=DeviceStatus.DETECTED,
                        description="Detected during 1-Wire scan.",
                        metadata={
                            "rom": rom,
                        },
                    )
                )

            return Result(
                success=True,
                message=f"Found {len(devices)} 1-Wire device(s).",
                devices=devices,
            )

        except Exception as exc:
            return Result(
                success=False,
                message="Failed to scan 1-Wire bus.",
                devices=[],
                error=exc,
            )
