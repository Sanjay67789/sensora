"""
Loads vendor and device definitions into the Sensora registry.
"""

from __future__ import annotations

from pathlib import Path

from sensora.database.factory import DefinitionFactory
from sensora.database.parser import YamlParser
from sensora.database.registry import DeviceRegistry
from sensora.database.validator import SchemaValidator

VENDORS_DIRECTORY = "vendors"
DEVICES_DIRECTORY = "devices"
SCHEMAS_DIRECTORY = "schemas"


class DatabaseLoader:
    """
    Loads all hardware definitions into an in-memory registry.
    """

    def __init__(
        self,
        definitions_path: Path | str = "definitions",
    ) -> None:
        self._definitions_path = Path(definitions_path).resolve()

        self._parser = YamlParser()
        self._validator = SchemaValidator(self.schemas_path)
        self._factory = DefinitionFactory()

    @property
    def definitions_path(self) -> Path:
        """
        Root definitions directory.
        """
        return self._definitions_path

    @property
    def vendors_path(self) -> Path:
        """
        Vendor definitions directory.
        """
        return self.definitions_path / VENDORS_DIRECTORY

    @property
    def devices_path(self) -> Path:
        """
        Device definitions directory.
        """
        return self.definitions_path / DEVICES_DIRECTORY

    @property
    def schemas_path(self) -> Path:
        """
        JSON schema directory.
        """
        return self.definitions_path / SCHEMAS_DIRECTORY

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def load(self) -> DeviceRegistry:
        """
        Load every vendor and device definition.

        Returns
        -------
        DeviceRegistry
            Populated registry.
        """
        self._validate_directory_structure()

        registry = DeviceRegistry()

        self._load_vendor_definitions(registry)
        self._load_device_definitions(registry)

        return registry

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def _validate_directory_structure(self) -> None:
        """
        Validate the expected directory structure.
        """
        required = (
            self.definitions_path,
            self.vendors_path,
            self.devices_path,
            self.schemas_path,
        )

        for directory in required:
            if not directory.is_dir():
                raise FileNotFoundError(f"Directory not found: {directory}")

    # ------------------------------------------------------------------
    # Vendor loading
    # ------------------------------------------------------------------

    def _load_vendor_definitions(
        self,
        registry: DeviceRegistry,
    ) -> None:
        """
        Load every vendor definition.
        """
        for file_path in sorted(self.vendors_path.glob("*.yaml")):
            self._load_vendor_definition(
                file_path,
                registry,
            )

    def _load_vendor_definition(
        self,
        file_path: Path,
        registry: DeviceRegistry,
    ) -> None:
        """
        Load a single vendor definition.
        """
        definition = self._parser.load(file_path)

        self._validator.validate_vendor(definition)

        vendor = self._factory.create_vendor(definition)

        registry.register_vendor(vendor)

    # ------------------------------------------------------------------
    # Device loading
    # ------------------------------------------------------------------

    def _load_device_definitions(
        self,
        registry: DeviceRegistry,
    ) -> None:
        """
        Load every device definition.
        """
        for file_path in sorted(self.devices_path.rglob("*.yaml")):
            self._load_device_definition(
                file_path,
                registry,
            )

    def _load_device_definition(
        self,
        file_path: Path,
        registry: DeviceRegistry,
    ) -> None:
        """
        Load a single device definition.
        """
        definition = self._parser.load(file_path)

        self._validator.validate_device(definition)

        device = self._factory.create_device(definition)

        registry.register_device(device)
