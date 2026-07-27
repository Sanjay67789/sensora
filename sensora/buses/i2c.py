"""
Abstract I²C communication bus interface.
"""

from __future__ import annotations

from abc import abstractmethod

from sensora.buses.base import BaseBus
from sensora.buses.discovery import ScannableBus


class I2CBus(BaseBus, ScannableBus):
    """
    Abstract base class for I²C communication buses.

    Platform-specific I²C backends should inherit from this class.
    """

    __slots__ = ()

    # ------------------------------------------------------------------
    # Device Communication
    # ------------------------------------------------------------------

    @abstractmethod
    def read_byte(
        self,
        address: int,
    ) -> int:
        """
        Read a single byte from a device.

        Parameters
        ----------
        address
            7-bit I²C device address.

        Returns
        -------
        int
            Byte read from the device.
        """
        raise NotImplementedError

    @abstractmethod
    def write_byte(
        self,
        address: int,
        value: int,
    ) -> None:
        """
        Write a single byte to a device.

        Parameters
        ----------
        address
            7-bit I²C device address.

        value
            Byte to write.
        """
        raise NotImplementedError

    @abstractmethod
    def read_register(
        self,
        address: int,
        register: int,
    ) -> int:
        """
        Read a device register.

        Parameters
        ----------
        address
            7-bit I²C device address.

        register
            Register address.

        Returns
        -------
        int
            Register value.
        """
        raise NotImplementedError

    @abstractmethod
    def write_register(
        self,
        address: int,
        register: int,
        value: int,
    ) -> None:
        """
        Write a device register.

        Parameters
        ----------
        address
            7-bit I²C device address.

        register
            Register address.

        value
            Value to write.
        """
        raise NotImplementedError

    @abstractmethod
    def read_block(
        self,
        address: int,
        register: int,
        length: int,
    ) -> bytes:
        """
        Read multiple bytes from a device.

        Parameters
        ----------
        address
            7-bit I²C device address.

        register
            Starting register.

        length
            Number of bytes to read.

        Returns
        -------
        bytes
            Bytes read from the device.
        """
        raise NotImplementedError

    @abstractmethod
    def write_block(
        self,
        address: int,
        register: int,
        data: bytes,
    ) -> None:
        """
        Write multiple bytes to a device.

        Parameters
        ----------
        address
            7-bit I²C device address.

        register
            Starting register.

        data
            Bytes to write.
        """
        raise NotImplementedError
