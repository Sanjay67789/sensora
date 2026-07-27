"""
Factory classes for creating Sensora database models.
"""

from __future__ import annotations

from typing import Any

from sensora.database.models import (
    DeviceDefinition,
    VendorDefinition,
)


class DefinitionFactory:
    """
    Creates database objects from parsed YAML data.
    """

    # ------------------------------------------------------------------
    # Vendor
    # ------------------------------------------------------------------

    def create_vendor(
        self,
        data: dict[str, Any],
    ) -> VendorDefinition:
        """
        Create a VendorDefinition object.
        """

        return VendorDefinition(
            id=data["id"],
            name=data["name"],
            description=data.get(
                "description",
                "",
            ),
            metadata=data.get(
                "metadata",
                {},
            ),
        )

    # ------------------------------------------------------------------
    # Device
    # ------------------------------------------------------------------

    def create_device(
        self,
        data: dict[str, Any],
    ) -> DeviceDefinition:
        """
        Create a DeviceDefinition object.

        Supports:

        New format:
            interfaces
            identification
            driver

        Legacy format:
            buses
            addresses
            chip_id
            driver_module
        """

        return DeviceDefinition(
            id=data["id"],
            name=data["name"],
            vendor=data["vendor"],
            description=data.get(
                "description",
                "",
            ),
            interfaces=self._interfaces(data),
            identification=self._identification(data),
            driver=self._driver(data),
            linux=data.get(
                "linux",
                {},
            ),
            measurements=data.get(
                "measurements",
                [],
            ),
            electrical=data.get(
                "electrical",
                {},
            ),
            package=data.get(
                "package",
                {},
            ),
            features=data.get(
                "features",
                {},
            ),
            metadata=data.get(
                "metadata",
                {},
            ),
        )

    # ------------------------------------------------------------------
    # Compatibility conversion
    # ------------------------------------------------------------------

    def _interfaces(
        self,
        data: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Convert legacy bus definitions.
        """

        if "interfaces" in data:
            return data["interfaces"]

        interfaces: dict[str, Any] = {}

        for bus in data.get(
            "buses",
            [],
        ):
            interfaces[bus] = {
                "supported": True,
                "addresses": data.get(
                    "addresses",
                    [],
                ),
            }

        return interfaces

    def _identification(
        self,
        data: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Convert legacy chip_id definition.
        """

        if "identification" in data:
            return data["identification"]

        if "chip_id" in data:
            return {
                "method": "register",
                "expected": data["chip_id"],
            }

        return {
            "method": "manual",
        }

    def _driver(
        self,
        data: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Convert legacy driver_module definition.
        """

        if "driver" in data:
            return data["driver"]

        return {
            "module": data.get(
                "driver_module",
                "",
            ),
            "class": data.get(
                "name",
                "",
            ),
        }
