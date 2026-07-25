"""Unified discovery interface for Sensora."""

from __future__ import annotations

from sensora.core.device import Device
from sensora.discovery.base import BaseScanner


class Scanner:
    """Coordinates all registered discovery scanners."""

    def __init__(self) -> None:
        self._scanners: list[BaseScanner] = []

    def register(self, scanner: BaseScanner) -> None:
        """Register a discovery scanner."""
        self._scanners.append(scanner)

    def scan(self) -> list[Device]:
        """Run all registered scanners."""

        devices: list[Device] = []

        for scanner in self._scanners:
            result = scanner.scan()

            if result.success:
                devices.extend(result.devices)

        return devices
