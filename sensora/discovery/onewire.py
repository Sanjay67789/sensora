"""
1-Wire device scanner.
"""

from __future__ import annotations

from sensora.buses.exceptions import BusError
from sensora.buses.onewire import OneWireBus
from sensora.core.device import Device
from sensora.core.result import Result
from sensora.database.matcher import DeviceMatcher
from sensora.discovery.base import BaseScanner


class OneWireScanner(BaseScanner):
    """
    Discover devices on a 1-Wire bus.
    """

    def __init__(
        self,
        bus: OneWireBus,
        matcher: DeviceMatcher,
    ) -> None:
        self._bus = bus
        self._matcher = matcher

    @property
    def name(self) -> str:
        """
        Human-readable scanner name.
        """
        return "1-Wire"

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

                family_code = rom.split("-")[0].upper()

                device = self._matcher.match_onewire(
                    family_code=family_code,
                    rom=rom,
                )

                if device is None:
                    device = self._matcher.create_unknown_onewire(
                        rom=rom,
                    )

                devices.append(device)

            return Result(
                success=True,
                message=f"Found {len(devices)} 1-Wire device(s).",
                devices=devices,
            )

        except BusError as exc:
            return Result(
                success=False,
                message="Failed to scan 1-Wire bus.",
                devices=[],
                error=exc,
            )
