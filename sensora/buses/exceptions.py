"""
Exceptions for the Sensora bus layer.
"""

from __future__ import annotations


class BusError(Exception):
    """
    Base exception for all bus-related errors.
    """


class BusNotOpenError(BusError):
    """
    Raised when an operation requires an open bus.
    """


class BusAlreadyOpenError(BusError):
    """
    Raised when attempting to open an already-open bus.
    """


class DeviceCommunicationError(BusError):
    """
    Raised when communication with a device fails.
    """


class InvalidAddressError(BusError):
    """
    Raised when an invalid device address is supplied.
    """


class InvalidRegisterError(BusError):
    """
    Raised when an invalid register address is supplied.
    """


class InvalidDataError(BusError):
    """
    Raised when invalid data is supplied to a bus operation.
    """


class BusScanError(BusError):
    """
    Raised when a bus scan fails.
    """
