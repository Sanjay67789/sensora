"""
Abstract SPI bus interface.
"""

from __future__ import annotations

from abc import abstractmethod

from sensora.buses.base import BaseBus


class SPIBus(BaseBus):
    """
    Abstract interface for SPI bus implementations.
    """

    @abstractmethod
    def transfer(
        self,
        data: bytes,
    ) -> bytes:
        """
        Perform a full-duplex SPI transfer.
        """
        raise NotImplementedError

    @abstractmethod
    def write(
        self,
        data: bytes,
    ) -> None:
        """
        Write bytes to the SPI device.
        """
        raise NotImplementedError

    @abstractmethod
    def read(
        self,
        length: int,
    ) -> bytes:
        """
        Read bytes from the SPI device.
        """
        raise NotImplementedError
