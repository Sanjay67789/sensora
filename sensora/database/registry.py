"""
In-memory registry for Sensora device definitions.
"""

from __future__ import annotations

from sensora.database.exceptions import (
    DuplicateDefinitionError,
)
from sensora.database.models import (
    DeviceDefinition,
    VendorDefinition,
)


class DeviceRegistry:
    """
    Stores all loaded vendor and device definitions.
    """

    def __init__(self) -> None:
        self._vendors: dict[str, VendorDefinition] = {}
        self._devices: dict[str, DeviceDefinition] = {}

    # ------------------------------------------------------------------
    # Vendor API
    # ------------------------------------------------------------------

    def register_vendor(self, vendor: VendorDefinition) -> None:
        """
        Register a vendor.
        """

        if vendor.vendor_id in self._vendors:
            raise DuplicateDefinitionError(
                f"Vendor '{vendor.vendor_id}' is already registered."
            )

        self._vendors[vendor.vendor_id] = vendor

    def get_vendor(self, vendor_id: str) -> VendorDefinition | None:
        """
        Return a vendor by its identifier.
        """

        return self._vendors.get(vendor_id)

    @property
    def vendors(self) -> tuple[VendorDefinition, ...]:
        """
        Return all registered vendors.
        """

        return tuple(self._vendors.values())

    # ------------------------------------------------------------------
    # Device API
    # ------------------------------------------------------------------

    def register_device(self, device: DeviceDefinition) -> None:
        """
        Register a device.
        """

        if device.device_id in self._devices:
            raise DuplicateDefinitionError(
                f"Device '{device.device_id}' is already registered."
            )

        self._devices[device.device_id] = device

    def get_device(self, device_id: str) -> DeviceDefinition | None:
        """
        Return a device by its identifier.
        """

        return self._devices.get(device_id)

    @property
    def devices(self) -> tuple[DeviceDefinition, ...]:
        """
        Return all registered devices.
        """

        return tuple(self._devices.values())

    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------

    def clear(self) -> None:
        """
        Remove all registered definitions.
        """

        self._vendors.clear()
        self._devices.clear()

    @property
    def vendor_count(self) -> int:
        return len(self._vendors)

    @property
    def device_count(self) -> int:
        return len(self._devices)
