"""
Device identification engine for Sensora.
"""

from __future__ import annotations

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
        Match an I2C device using its address.

        Parameters
        ----------
        address
            Detected 7-bit I2C address.

        Returns
        -------
        Device | None
            Identified device or None.
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
                )

        return None

    def _match_address(
        self,
        addresses,
        address: str,
    ) -> bool:
        """
        Check address compatibility.
        """

        if isinstance(addresses, list):
            return address in addresses

        if isinstance(addresses, dict):

            for value in addresses.values():

                if isinstance(value, list) and address in value:
                    return True

                if isinstance(value, str) and address == value:
                    return True

        return False

    def _create_device(
        self,
        definition,
        address: int,
    ) -> Device:
        """
        Convert database definition into runtime Device.
        """

        bus = BusType.I2C

        if definition.buses:

            try:
                bus = BusType(definition.buses[0])

            except ValueError:
                bus = BusType.I2C

        return Device(
            name=definition.name,
            manufacturer=definition.vendor,
            bus=bus,
            address=address,
            status=DeviceStatus.DETECTED,
            description=definition.description,
            metadata={
                "definition_id": definition.id,
                "identified": True,
            },
        )
