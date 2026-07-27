"""
JSON Schema validator for Sensora definition files.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, ValidationError

from sensora.database.exceptions import SchemaValidationError


class SchemaValidator:
    """
    Validates vendor and device definitions against JSON Schemas.
    """

    DEVICE_SCHEMA = "device.schema.json"
    VENDOR_SCHEMA = "vendor.schema.json"

    def __init__(self, schemas_path: Path | str) -> None:
        """
        Initialize the schema validator.

        Parameters
        ----------
        schemas_path
            Path to the directory containing JSON Schema files.
        """
        self._schemas_path = Path(schemas_path).resolve()

        self._device_validator = self._load_validator(self.DEVICE_SCHEMA)
        self._vendor_validator = self._load_validator(self.VENDOR_SCHEMA)

    @property
    def schemas_path(self) -> Path:
        """
        Return the schema directory.
        """
        return self._schemas_path

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def validate_device(
        self,
        definition: dict[str, Any],
    ) -> None:
        """
        Validate a device definition.

        Parameters
        ----------
        definition
            Parsed device definition.

        Raises
        ------
        SchemaValidationError
            If the definition does not conform to the schema.
        """
        try:
            self._device_validator.validate(definition)
        except ValidationError as exc:
            raise SchemaValidationError(
                f"Invalid device definition: {exc.message}"
            ) from exc

    def validate_vendor(
        self,
        definition: dict[str, Any],
    ) -> None:
        """
        Validate a vendor definition.

        Parameters
        ----------
        definition
            Parsed vendor definition.

        Raises
        ------
        SchemaValidationError
            If the definition does not conform to the schema.
        """
        try:
            self._vendor_validator.validate(definition)
        except ValidationError as exc:
            raise SchemaValidationError(
                f"Invalid vendor definition: {exc.message}"
            ) from exc

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _load_validator(
        self,
        schema_name: str,
    ) -> Draft202012Validator:
        """
        Load and compile a JSON Schema validator.

        Parameters
        ----------
        schema_name
            JSON Schema filename.

        Returns
        -------
        Draft202012Validator
            Compiled validator.

        Raises
        ------
        FileNotFoundError
            If the schema file does not exist.

        SchemaValidationError
            If the schema itself is invalid.
        """
        schema_path = self.schemas_path / schema_name

        if not schema_path.is_file():
            raise FileNotFoundError(f"Schema not found: {schema_path}")

        with schema_path.open(
            "r",
            encoding="utf-8",
        ) as file:
            schema = json.load(file)

        try:
            Draft202012Validator.check_schema(schema)
        except Exception as exc:
            raise SchemaValidationError(
                f"Invalid schema '{schema_name}': {exc}"
            ) from exc

        return Draft202012Validator(schema)
