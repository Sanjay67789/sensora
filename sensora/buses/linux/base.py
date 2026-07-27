"""
Linux backend base classes for Sensora.

This module provides the common functionality shared by all Linux
communication bus backends.
"""

from __future__ import annotations

from abc import ABC
from pathlib import Path

from sensora.buses.base import BaseBus
from sensora.buses.exceptions import (
    BusAlreadyOpenError,
    BusNotOpenError,
)


class LinuxBus(BaseBus, ABC):
    """
    Base class for all Linux communication bus backends.

    This class provides common lifecycle state management and validation
    helpers. Protocol-specific implementations should inherit from this
    class and implement only their communication logic.
    """

    __slots__ = ("_is_open",)

    def __init__(self) -> None:
        """Initialize the backend."""
        self._is_open = False

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def is_open(self) -> bool:
        """Return whether the backend is currently open."""
        return self._is_open

    # ------------------------------------------------------------------
    # Lifecycle helpers
    # ------------------------------------------------------------------

    def _set_open(self, state: bool) -> None:
        """
        Update the backend open state.

        Parameters
        ----------
        state
            True if the backend is open.
        """
        self._is_open = state

    def _validate_open(self) -> None:
        """
        Ensure the backend is open.

        Raises
        ------
        BusNotOpenError
            If the backend has not been opened.
        """
        if not self._is_open:
            raise BusNotOpenError(f"{self.name} is not open.")

    def _validate_closed(self) -> None:
        """
        Ensure the backend is closed.

        Raises
        ------
        BusAlreadyOpenError
            If the backend is already open.
        """
        if self._is_open:
            raise BusAlreadyOpenError(f"{self.name} is already open.")

    # ------------------------------------------------------------------
    # Filesystem helpers
    # ------------------------------------------------------------------

    @staticmethod
    def validate_device_path(path: str | Path) -> Path:
        """
        Validate that a Linux device path exists.

        Parameters
        ----------
        path
            Device file or sysfs path.

        Returns
        -------
        Path
            The validated device path.

        Raises
        ------
        FileNotFoundError
            If the path does not exist.
        """
        device = Path(path)

        if not device.exists():
            raise FileNotFoundError(f"Device '{device}' does not exist.")

        return device
