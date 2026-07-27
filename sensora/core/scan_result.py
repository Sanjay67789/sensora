"""
Discovery scan result models for Sensora.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from sensora.core.device import Device


@dataclass(slots=True)
class BusResult:
    """
    Result of scanning a single hardware bus.
    """

    name: str
    success: bool

    devices: list[Device] = field(default_factory=list)

    message: str = ""


@dataclass(slots=True)
class ScanResult:
    """
    Complete hardware discovery result.
    """

    buses: list[BusResult] = field(default_factory=list)

    duration: float = 0.0

    warnings: list[str] = field(default_factory=list)

    @property
    def devices(self) -> list[Device]:
        """
        Return every discovered device from all buses.
        """

        devices: list[Device] = []

        for bus in self.buses:
            devices.extend(bus.devices)

        return devices

    @property
    def device_count(self) -> int:
        """
        Return the total number of discovered devices.
        """
        return len(self.devices)

    @property
    def success(self) -> bool:
        """
        True if at least one bus completed successfully.
        """
        return any(bus.success for bus in self.buses)
