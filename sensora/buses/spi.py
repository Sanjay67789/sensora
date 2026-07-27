"""
Abstract SPI communication bus interface.
"""

from __future__ import annotations

from abc import abstractmethod

from sensora.buses.base import BaseBus
from sensora.buses.discovery import ScannableBus


class SPIBus(BaseBus, ScannableBus):
    """
    Abstract base class for SPI communication buses.

    Platform-specific SPI backends should inherit from this class.
    """

    __slots__ = ()

    # ------------------------------------------------------------------
    # Device Communication
    # ------------------------------------------------------------------

    @abstractmethod
    def transfer(
        self,
        data: bytes,
    ) -> bytes:
        """
        Perform a full-duplex SPI transfer.

        Parameters
        ----------
        data
            Bytes to transmit.

        Returns
        -------
        bytes
            Bytes received from the slave device.
        """
        raise NotImplementedError

    @abstractmethod
    def read(
        self,
        length: int,
    ) -> bytes:
        """
        Read bytes from the SPI device.

        Parameters
        ----------
        length
            Number of bytes to read.

        Returns
        -------
        bytes
            Bytes read from the device.
        """
        raise NotImplementedError

    @abstractmethod
    def write(
        self,
        data: bytes,
    ) -> None:
        """
        Write bytes to the SPI device.

        Parameters
        ----------
        data
            Bytes to transmit.
        """
        raise NotImplementedError
