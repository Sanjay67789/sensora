"""
Abstract base classes for Sensora hardware communication buses.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Self


class BaseBus(ABC):
    """
    Abstract base class for all hardware communication buses.

    A bus implementation is responsible only for managing the
    communication channel. Device discovery and protocol-specific
    operations are defined by specialized interfaces.
    """

    def __enter__(self) -> Self:
        """Open the bus when entering a context manager."""
        self.open()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: object | None,
    ) -> None:
        """Close the bus when leaving a context manager."""
        self.close()

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable bus name."""
        raise NotImplementedError

    @property
    @abstractmethod
    def bus_type(self) -> str:
        """Bus type identifier."""
        raise NotImplementedError

    @property
    @abstractmethod
    def is_open(self) -> bool:
        """Return True if the bus is currently open."""
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    @abstractmethod
    def open(self) -> None:
        """Open the communication channel."""
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        """Close the communication channel."""
        raise NotImplementedError

    def reset(self) -> None:
        """
        Reset the communication channel.

        The default implementation closes and reopens the bus.
        """
        self.close()
        self.open()
