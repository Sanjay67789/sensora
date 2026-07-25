"""Unified discovery interface for Sensora."""

from __future__ import annotations

from sensora.core.device import Device
from sensora.discovery.base import BaseScanner


class Scanner:
    """
    Coordinates all registered discovery scanners.

    Example:
        scanner = Scanner()
        scanner.register(I2CScanner())
        scanner.register(SPIScanner())

        devices = scanner.scan_all()
    """

    def __init__(self) -> None:
        """Initialize an empty scanner registry."""
        self._scanners: list[BaseScanner] = []

    def register(self, scanner: BaseScanner) -> None:
        """
        Register a discovery scanner.

        Args:
            scanner: A scanner implementing BaseScanner.
        """
        self._scanners.append(scanner)

    def scan_all(self) -> list[Device]:
        """
        Run every registered scanner.

        Returns:
            A list containing all discovered devices.
        """
        devices: list[Device] = []

        for scanner in self._scanners:
            result = scanner.scan()

            if result.success:
                devices.extend(result.devices)

        return devices
