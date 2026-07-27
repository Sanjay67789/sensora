"""
UART device discovery for Sensora.
"""

from __future__ import annotations

import os
from pathlib import Path

from sensora.core.device import Device
from sensora.core.enums import BusType, DeviceStatus
from sensora.core.result import Result
from sensora.discovery.base import BaseScanner


class UARTScanner(BaseScanner):
    """
    Discover Linux UART devices.

    This scanner enumerates serial devices exposed by Linux.
    """

    # Real user-accessible serial devices
    DEVICE_PATTERNS = (
        "ttyUSB*",
        "ttyACM*",
        "ttyAMA*",
        "ttyTHS*",
    )

    # Optional hardware UARTs
    OPTIONAL_PATTERNS = ("ttyS*",)

    def __init__(
        self,
        dev_directory: Path | str = "/dev",
        include_kernel_uart: bool = False,
    ) -> None:
        self._dev_directory = Path(dev_directory)
        self._include_kernel_uart = include_kernel_uart

    @property
    def name(self) -> str:
        return "UART"

    def scan(self) -> Result:
        """
        Scan Linux serial devices.
        """

        devices: list[Device] = []
        seen: set[Path] = set()

        try:
            patterns = list(self.DEVICE_PATTERNS)

            if self._include_kernel_uart:
                patterns.extend(self.OPTIONAL_PATTERNS)

            for pattern in patterns:
                for path in sorted(self._dev_directory.glob(pattern)):
                    if path in seen:
                        continue

                    if not self._is_device(path):
                        continue

                    seen.add(path)

                    devices.append(self._create_device(path))

            return Result(
                success=True,
                message=f"Found {len(devices)} UART device(s).",
                devices=devices,
            )

        except OSError as exc:
            return Result(
                success=False,
                message="Failed to enumerate UART devices.",
                devices=[],
                error=exc,
            )

    def _is_device(
        self,
        path: Path,
    ) -> bool:
        """
        Check whether the path is a usable serial device.
        """

        try:
            return path.exists() and os.access(
                path,
                os.R_OK | os.W_OK,
            )

        except OSError:
            return False

    def _create_device(
        self,
        path: Path,
    ) -> Device:
        return Device(
            name=path.name,
            bus=BusType.UART,
            status=DeviceStatus.DETECTED,
            description="Linux UART device",
            metadata={
                "device": str(path),
            },
        )
