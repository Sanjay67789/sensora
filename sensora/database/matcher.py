"""
Device identification engine for Sensora.
"""

from __future__ import annotations

from sensora.core.device import Device
from sensora.core.enums import BusType, DeviceStatus
from sensora.database.models import DeviceDefinition
from sensora.database.registry import DeviceRegistry


class DeviceMatcher:
    """
    Matches discovered hardware devices against
    Sensora device definitions.
    """

    def __init__(
        self,
        registry: DeviceRegistry,
    ) -> None:
        self._registry = registry

    # ------------------------------------------------------------------
    # I²C
    # ------------------------------------------------------------------

    def match_i2c(
        self,
        address: int,
    ) -> Device | None:
        """
        Match an I²C device using its address.
        """

        definition = self._registry.find_i2c_device(address)

        if definition is None:
            return None

        return self._create_device(
            definition=definition,
            address=address,
            bus=BusType.I2C,
        )

    # ------------------------------------------------------------------
    # Unknown devices
    # ------------------------------------------------------------------

    def create_unknown_i2c(
        self,
        address: int,
    ) -> Device:
        """
        Create an unidentified I²C device.
        """

        return Device(
            name=f"Unknown I²C Device (0x{address:02X})",
            manufacturer=None,
            bus=BusType.I2C,
            address=address,
            status=DeviceStatus.UNKNOWN,
            description="No matching database definition found.",
            metadata={
                "identified": False,
            },
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _create_device(
        self,
        definition: DeviceDefinition,
        address: int,
        bus: BusType,
    ) -> Device:
        """
        Convert a database definition into a runtime Device.
        """

        detected_bus = bus

        for interface_name in definition.interfaces:
            try:
                detected_bus = BusType(interface_name)
                break
            except ValueError:
                continue

        return Device(
            name=definition.name,
            manufacturer=definition.vendor,
            bus=detected_bus,
            address=address,
            chip_id=None,
            status=DeviceStatus.IDENTIFIED,
            description=definition.description,
            metadata={
                "definition_id": definition.id,
                "identified": True,
                "interfaces": definition.interfaces,
                "identification": definition.identification,
                "driver": definition.driver,
                "linux": definition.linux,
                "measurements": definition.measurements,
                "electrical": definition.electrical,
                "package": definition.package,
                "features": definition.features,
                "metadata": definition.metadata,
            },
        )
