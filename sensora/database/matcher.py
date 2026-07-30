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
            bus=BusType.I2C,
            address=address,
        )

    # ------------------------------------------------------------------
    # 1-Wire
    # ------------------------------------------------------------------

    def match_onewire(
        self,
        family_code: str,
        rom: str,
    ) -> Device | None:
        """
        Match a 1-Wire device using its family code.
        """

        definition = self._registry.find_onewire_device(family_code)

        if definition is None:
            return None

        return self._create_device(
            definition=definition,
            bus=BusType.ONEWIRE,
            rom=rom,
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

    def create_unknown_onewire(
        self,
        rom: str,
    ) -> Device:
        """
        Create an unidentified 1-Wire device.
        """

        family_code = rom.split("-")[0].upper()

        return Device(
            name="Unknown 1-Wire Device",
            manufacturer=None,
            bus=BusType.ONEWIRE,
            status=DeviceStatus.UNKNOWN,
            description="No matching database definition found.",
            metadata={
                "identified": False,
                "rom": rom,
                "family_code": family_code,
            },
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _create_device(
        self,
        definition: DeviceDefinition,
        bus: BusType,
        address: int | None = None,
        rom: str | None = None,
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

        metadata = {
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
        }

        if definition.metadata:
            metadata.update(definition.metadata)

        if rom is not None:
            metadata["rom"] = rom
            metadata["family_code"] = rom.split("-")[0].upper()

        return Device(
            name=definition.name,
            manufacturer=definition.vendor,
            bus=detected_bus,
            address=address,
            chip_id=None,
            status=DeviceStatus.IDENTIFIED,
            description=definition.description,
            metadata=metadata,
        )
