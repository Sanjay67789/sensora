"""
Loads hardware definitions into the Sensora database.
"""

from __future__ import annotations

from pathlib import Path

from sensora.database.registry import DeviceRegistry


class DatabaseLoader:
    """
    Loads vendor and device definitions from the filesystem.
    """

    def __init__(self, definitions_path: Path | str = "definitions") -> None:
        self._definitions_path = Path(definitions_path)

    @property
    def definitions_path(self) -> Path:
        """
        Root definitions directory.
        """
        return self._definitions_path

    @property
    def vendors_path(self) -> Path:
        """
        Vendor definition directory.
        """
        return self._definitions_path / "vendors"

    @property
    def devices_path(self) -> Path:
        """
        Device definition directory.
        """
        return self._definitions_path / "devices"

    @property
    def schemas_path(self) -> Path:
        """
        Schema definition directory.
        """
        return self._definitions_path / "schemas"

    def load(self) -> DeviceRegistry:
        """
        Load all hardware definitions.

        Returns
        -------
        DeviceRegistry
            Registry containing all loaded definitions.
        """
        registry = DeviceRegistry()

        self._load_vendors(registry)
        self._load_devices(registry)

        return registry

    # ------------------------------------------------------------------
    # Internal loading methods
    # ------------------------------------------------------------------

    def _load_vendors(self, registry: DeviceRegistry) -> None:
        """
        Load all vendor definitions.
        """
        if not self.vendors_path.exists():
            return

        for _file in sorted(self.vendors_path.glob("*.yaml")):
            # TODO:
            # Parse YAML
            # Validate schema
            # Create VendorDefinition
            # registry.register_vendor(...)
            pass

    def _load_devices(self, registry: DeviceRegistry) -> None:
        """
        Load all device definitions.
        """
        if not self.devices_path.exists():
            return

        for _file in sorted(self.devices_path.rglob("*.yaml")):
            # TODO:
            # Parse YAML
            # Validate schema
            # Create DeviceDefinition
            # registry.register_device(...)
            pass
