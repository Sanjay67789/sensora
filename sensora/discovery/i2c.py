"""
I²C device discovery for Linux.
"""

from __future__ import annotations

import time
from pathlib import Path

from sensora.buses.exceptions import BusError
from sensora.buses.linux.i2c import LinuxI2CBus
from sensora.core.device import Device
from sensora.core.enums import BusType, DeviceStatus
from sensora.core.result import Result
from sensora.database.matcher import DeviceMatcher
from sensora.discovery.base import BaseScanner


class I2CScanner(BaseScanner):
    """
    Discover devices connected to all available Linux I²C adapters.
    """

    def __init__(
        self,
        matcher: DeviceMatcher | None = None,
        device_directory: str | Path = "/dev",
    ) -> None:
        self._device_directory = Path(device_directory)
        self._matcher = matcher

    @property
    def name(self) -> str:
        """Return the scanner name."""
        return "I²C"

    def scan(self) -> Result:
        """
        Scan every Linux I²C adapter.
        """

        devices: list[Device] = []

        scanned_buses = 0
        failed_buses = 0

        adapters = sorted(self._device_directory.glob("i2c-*"))

        if not adapters:
            return Result(
                success=True,
                message="No Linux I²C adapters found.",
            )

        for adapter in adapters:

            bus_start = time.perf_counter()

            try:
                bus_id = int(adapter.name.removeprefix("i2c-"))

            except ValueError:
                continue

            bus = LinuxI2CBus(bus_id)

            try:
                bus.open()

                scanned_buses += 1

                addresses = bus.scan()

                scan_time = time.perf_counter() - bus_start

                for address in addresses:

                    device = None

                    # Try database identification
                    if self._matcher:

                        device = self._matcher.match_i2c(address)

                    # Unknown fallback
                    if device is None:

                        device = Device(
                            name=f"I²C Device (0x{address:02X})",
                            manufacturer=None,
                            bus=BusType.I2C,
                            address=address,
                            status=DeviceStatus.DETECTED,
                            description=("Detected during I²C scan."),
                            metadata={},
                        )

                    device.metadata.update(
                        {
                            "bus_id": bus_id,
                            "device": str(adapter),
                            "scan_time": (f"{scan_time:.3f}s"),
                        }
                    )

                    devices.append(device)

            except BusError:

                failed_buses += 1

            finally:

                if bus.is_open:
                    bus.close()

        return Result(
            success=True,
            message=(
                f"Scanned {scanned_buses} bus(es), " f"found {len(devices)} device(s)."
            ),
            devices=devices,
            data={
                "buses_scanned": scanned_buses,
                "buses_failed": failed_buses,
            },
        )
