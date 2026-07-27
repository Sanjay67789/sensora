"""
Factory for creating Sensora database models from validated definitions.
"""

from __future__ import annotations

from typing import Any

from sensora.database.models import DeviceDefinition, VendorDefinition


class DefinitionFactory:
    """
    Factory responsible for creating database model instances.

    The input dictionaries are assumed to have already been validated
    against the appropriate JSON Schema.
    """

    def create_vendor(
        self,
        definition: dict[str, Any],
    ) -> VendorDefinition:
        """
        Create a VendorDefinition.

        Parameters
        ----------
        definition
            Validated vendor definition.

        Returns
        -------
        VendorDefinition
        """
        return VendorDefinition(
            id=definition["id"],
            name=definition["name"],
            description=definition.get("description", ""),
            metadata=definition.get("metadata", {}),
        )

    def create_device(
        self,
        definition: dict[str, Any],
    ) -> DeviceDefinition:
        """
        Create a DeviceDefinition.

        Parameters
        ----------
        definition
            Validated device definition.

        Returns
        -------
        DeviceDefinition
        """
        return DeviceDefinition(
            id=definition["id"],
            name=definition["name"],
            vendor=definition["vendor"],
            description=definition.get("description", ""),
            interfaces=definition["interfaces"],
            identification=definition["identification"],
            driver=definition["driver"],
            linux=definition.get("linux", {}),
            measurements=definition.get("measurements", []),
            electrical=definition.get("electrical", {}),
            package=definition.get("package", {}),
            features=definition.get("features", {}),
            metadata=definition.get("metadata", {}),
        )
