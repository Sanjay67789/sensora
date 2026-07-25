"""I²C device discovery."""

from __future__ import annotations

from sensora.buses.i2c import I2CBus
from sensora.core.device import Device
from sensora.core.enums import BusType, DeviceStatus
from sensora.core.exceptions import DeviceCommunicationError
from sensora.core.result import Result
from sensora.discovery.base import BaseScanner
from sensora.discovery.probe import I2CProbe


class I2CScanner(BaseScanner):
    """Discover devices connected to an I²C bus."""

    def __init__(self, bus_id: int = 1) -> None:
        self._bus = I2CBus(bus_id)
        self._probe = I2CProbe(self._bus)

    def scan(self) -> Result:
        """Scan the I²C bus for responding devices."""

        devices: list[Device] = []

        opened_here = False

        if not self._bus.is_open:
            self._bus.open()
            opened_here = True

        try:
            for address in range(0x03, 0x78):
                if self._probe.exists(address):
                    devices.append(
                        Device(
                            name="Unknown I²C Device",
                            manufacturer="Unknown",
                            bus=BusType.I2C,
                            address=address,
                            chip_id=None,
                            status=DeviceStatus.DETECTED,
                            description="I²C device detected",
                        )
                    )

        except DeviceCommunicationError:
            return Result(
                success=False,
                message="Failed to scan the I²C bus.",
                devices=[],
            )

        finally:
            if opened_here:
                self._bus.close()

        return Result(
            success=True,
            message=f"Found {len(devices)} device(s).",
            devices=devices,
        )
