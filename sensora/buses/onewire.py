"""
Abstract 1-Wire bus interface.
"""

from __future__ import annotations

from abc import abstractmethod
from pathlib import Path

from sensora.buses.base import BaseBus


class OneWireBus(BaseBus):
    """
    Abstract interface for Linux-style 1-Wire buses.
    """

    @abstractmethod
    def scan(self) -> list[str]:
        """
        Discover connected devices.

        Returns
        -------
        list[str]
            List of device ROM identifiers.
        """
        raise NotImplementedError

    @abstractmethod
    def exists(
        self,
        rom: str,
    ) -> bool:
        """
        Return whether a device exists.
        """
        raise NotImplementedError

    @abstractmethod
    def device_path(
        self,
        rom: str,
    ) -> Path:
        """
        Return the filesystem path of a device.
        """
        raise NotImplementedError

    @abstractmethod
    def read_text(
        self,
        rom: str,
        filename: str,
    ) -> str:
        """
        Read a text attribute from a device.
        """
        raise NotImplementedError

    @abstractmethod
    def read_bytes(
        self,
        rom: str,
        filename: str,
    ) -> bytes:
        """
        Read a binary attribute from a device.
        """
        raise NotImplementedError
