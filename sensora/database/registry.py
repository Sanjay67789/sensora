"""
In-memory registry for Sensora device definitions.
"""

from __future__ import annotations

from sensora.database.exceptions import (
    DuplicateDefinitionError,
    VendorNotFoundError,
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

        Parameters
        ----------
        vendor
            Vendor definition to register.

        Raises
        ------
        DuplicateDefinitionError
            If the vendor is already registered.
        """
        if vendor.id in self._vendors:
            raise DuplicateDefinitionError(
                f"Vendor '{vendor.id}' is already registered."
            )

        self._vendors[vendor.id] = vendor

    def get_vendor(self, vendor_id: str) -> VendorDefinition | None:
        """
        Return a vendor by its identifier.

        Parameters
        ----------
        vendor_id
            Vendor identifier.

        Returns
        -------
        VendorDefinition | None
            Vendor if found, otherwise None.
        """
        return self._vendors.get(vendor_id)

    def require_vendor(self, vendor_id: str) -> VendorDefinition:
        """
        Return a vendor.

        Raises
        ------
        VendorNotFoundError
            If the vendor does not exist.
        """
        vendor = self.get_vendor(vendor_id)

        if vendor is None:
            raise VendorNotFoundError(f"Vendor '{vendor_id}' is not registered.")

        return vendor

    @property
    def vendors(self) -> tuple[VendorDefinition, ...]:
        """
        Return all registered vendors.
        """
        return tuple(self._vendors.values())

    @property
    def vendor_count(self) -> int:
        """
        Return the number of registered vendors.
        """
        return len(self._vendors)

    # ------------------------------------------------------------------
    # Device API
    # ------------------------------------------------------------------

    def register_device(self, device: DeviceDefinition) -> None:
        """
        Register a device.

        Parameters
        ----------
        device
            Device definition to register.

        Raises
        ------
        DuplicateDefinitionError
            If the device is already registered.
        """
        if device.id in self._devices:
            raise DuplicateDefinitionError(
                f"Device '{device.id}' is already registered."
            )

        if device.vendor not in self._vendors:
            raise VendorNotFoundError(f"Vendor '{device.vendor}' is not registered.")

        self._devices[device.id] = device

    def get_device(self, device_id: str) -> DeviceDefinition | None:
        """
        Return a device by its identifier.

        Parameters
        ----------
        device_id
            Device identifier.

        Returns
        -------
        DeviceDefinition | None
            Device if found, otherwise None.
        """
        return self._devices.get(device_id)

    @property
    def devices(self) -> tuple[DeviceDefinition, ...]:
        """
        Return all registered devices.
        """
        return tuple(self._devices.values())

    @property
    def device_count(self) -> int:
        """
        Return the number of registered devices.
        """
        return len(self._devices)

    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------

    def clear(self) -> None:
        """
        Remove all registered definitions.
        """
        self._vendors.clear()
        self._devices.clear()
