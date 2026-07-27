"""
Discovery interfaces for communication buses.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class ScannableBus(ABC):
    """
    Interface for buses that support device discovery.
    """

    @abstractmethod
    def scan(self) -> list[int]:
        """
        Discover devices connected to the bus.

        Returns
        -------
        list[int]
            A list of discovered device addresses.
        """
        raise NotImplementedError

    @abstractmethod
    def ping(self, address: int) -> bool:
        """
        Check whether a device responds at the given address.
        """
        raise NotImplementedError
