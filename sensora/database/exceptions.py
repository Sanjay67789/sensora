"""
Custom exceptions for the Sensora database.
"""


class DatabaseError(Exception):
    """Base exception for all database errors."""


class DefinitionError(DatabaseError):
    """Raised when a device definition is invalid."""


class DuplicateDefinitionError(DatabaseError):
    """Raised when duplicate definitions are found."""


class RegistryError(DatabaseError):
    """Raised when a registry operation fails."""


class SchemaValidationError(DatabaseError):
    """Raised when schema validation fails."""


class VendorNotFoundError(DatabaseError):
    """Raised when a referenced vendor does not exist."""
