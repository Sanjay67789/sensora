"""
Device identification engine for Sensora.
"""

from __future__ import annotations

from typing import Any

from sensora.core.device import Device
from sensora.core.enums import BusType, DeviceStatus
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

    def match_i2c(
        self,
        address: int,
    ) -> Device | None:
        """
        Match an I2C device using address.
        """

        address_hex = f"0x{address:02X}"

        for definition in self._registry.devices:

            if self._match_address(
                definition.addresses,
                address_hex,
            ):
                return self._create_device(
                    definition,
                    address,
                    BusType.I2C,
                )

        return None

    def create_unknown_i2c(
        self,
        address: int,
    ) -> Device:
        """
        Create an unidentified I2C device.
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

    def _match_address(
        self,
        addresses: Any,
        address: str,
    ) -> bool:
        """
        Check address compatibility.
        """

        if isinstance(addresses, list):
            return address in addresses

        if isinstance(addresses, dict):

            for values in addresses.values():

                if isinstance(values, list) and address in values:
                    return True

                if isinstance(values, str) and address == values:
                    return True

        return False

    def _create_device(
        self,
        definition: Any,
        address: int,
        bus: BusType,
    ) -> Device:
        """
        Convert database definition into runtime device.
        """

        detected_bus = bus

        if definition.buses:

            try:
                detected_bus = BusType(
                    definition.buses[0]
                )

            except ValueError:
                pass

        return Device(
            name=definition.name,
            manufacturer=definition.vendor,
            bus=detected_bus,
            address=address,
            status=DeviceStatus.IDENTIFIED,
            description=definition.description,
            metadata={
                "definition_id": definition.id,
                "identified": True,
                "measurements": definition.measurements,
            },
        )
