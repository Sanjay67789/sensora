"""Custom exceptions used throughout Sensora."""


class SensoraError(Exception):
    """Base exception for all Sensora errors."""


class BusError(SensoraError):
    """Raised when a hardware communication bus fails."""


class DiscoveryError(SensoraError):
    """Raised when device discovery fails."""


class DeviceError(SensoraError):
    """Base exception for device-related errors."""


class DeviceNotFoundError(DeviceError):
    """Raised when a requested device cannot be found."""


class DeviceCommunicationError(DeviceError):
    """Raised when communication with a device fails."""


class DatabaseError(SensoraError):
    """Raised for database-related errors."""


class PluginError(SensoraError):
    """Raised when a plugin encounters an error."""
