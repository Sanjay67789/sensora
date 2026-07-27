"""
Unified discovery interface for Sensora.
"""

from __future__ import annotations

import time

from sensora.core.scan_result import BusResult, ScanResult
from sensora.discovery.base import BaseScanner


class Scanner:
    """
    Coordinates all registered discovery scanners.
    """

    def __init__(self) -> None:
        self._scanners: list[BaseScanner] = []

    def register(self, scanner: BaseScanner) -> None:
        """
        Register a discovery scanner.
        """
        self._scanners.append(scanner)

    def clear(self) -> None:
        """
        Remove all registered scanners.
        """
        self._scanners.clear()

    def scan(self) -> ScanResult:
        """
        Execute every registered scanner and return a unified ScanResult.
        """

        start = time.perf_counter()

        result = ScanResult()

        for scanner in self._scanners:
            scan_result = scanner.scan()

            result.buses.append(
                BusResult(
                    name=scanner.name,
                    success=scan_result.success,
                    devices=scan_result.devices,
                    message=scan_result.message,
                )
            )

        result.duration = time.perf_counter() - start

        return result
