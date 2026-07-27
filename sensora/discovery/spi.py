"""
SPI device discovery for Sensora.
"""

from __future__ import annotations

from pathlib import Path

from sensora.core.device import Device
from sensora.core.enums import BusType, DeviceStatus
from sensora.core.result import Result
from sensora.discovery.base import BaseScanner


class SPIScanner(BaseScanner):
    """
    Discover Linux SPI devices.

    SPI has no discovery protocol. This scanner enumerates Linux
    spidev device nodes exposed by the kernel.
    """

    def __init__(self, dev_directory: Path | str = "/dev") -> None:
        self._dev_directory = Path(dev_directory)

    @property
    def name(self) -> str:
        """Human-readable scanner name."""
        return "SPI"

    def scan(self) -> Result:
        """
        Scan for Linux SPI device nodes.

        Returns
        -------
        Result
            Discovery result containing detected SPI devices.
        """
        devices: list[Device] = []

        try:
            for path in sorted(self._dev_directory.glob("spidev*")):
                devices.append(self._create_device(path))

            return Result(
                success=True,
                message=f"Found {len(devices)} SPI device(s).",
                devices=devices,
            )

        except OSError as exc:
            return Result(
                success=False,
                message="Failed to enumerate SPI devices.",
                error=exc,
            )

    def _create_device(self, path: Path) -> Device:
        """
        Create a Device model from a Linux spidev node.
        """
        bus = None
        chip_select = None

        try:
            _, suffix = path.name.split("spidev")
            bus_str, cs_str = suffix.split(".")
            bus = int(bus_str)
            chip_select = int(cs_str)
        except (ValueError, IndexError):
            pass

        return Device(
            name=path.name,
            bus=BusType.SPI,
            status=DeviceStatus.DETECTED,
            description="Linux SPI device",
            metadata={
                "device": str(path),
                "bus": bus,
                "chip_select": chip_select,
            },
        )
