"""Abstract base classes for hardware communication buses."""

from __future__ import annotations

from abc import ABC, abstractmethod


class BaseBus(ABC):
    """
    Abstract base class for all hardware communication buses.

    A bus implementation is responsible only for establishing and managing
    communication with a hardware interface. Device discovery and protocol-
    specific logic belong to higher-level components.
    """

    @abstractmethod
    def open(self) -> None:
        """
        Open the communication channel.

        Raises:
            BusError:
                If the bus cannot be opened.
        """
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        """
        Close the communication channel.

        This method should be safe to call multiple times.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def is_open(self) -> bool:
        """
        Return whether the communication channel is currently open.
        """
        raise NotImplementedError
