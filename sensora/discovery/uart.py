"""
UART device discovery for Sensora.
"""

from __future__ import annotations

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

    DEVICE_PATTERNS = (
        "ttyS*",
        "ttyUSB*",
        "ttyACM*",
        "ttyAMA*",
        "ttyTHS*",
    )

    def __init__(self, dev_directory: Path | str = "/dev") -> None:
        self._dev_directory = Path(dev_directory)

    @property
    def name(self) -> str:
        return "UART"

    def scan(self) -> Result:
        devices: list[Device] = []

        try:
            for pattern in self.DEVICE_PATTERNS:
                for path in sorted(self._dev_directory.glob(pattern)):
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
                error=exc,
            )

    def _create_device(self, path: Path) -> Device:
        return Device(
            name=path.name,
            bus=BusType.UART,
            status=DeviceStatus.DETECTED,
            description="Linux UART device",
            metadata={
                "device": str(path),
            },
        )
