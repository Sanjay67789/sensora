"""
Abstract UART communication bus interface.
"""

from __future__ import annotations

from abc import abstractmethod

from sensora.buses.base import BaseBus


class UARTBus(BaseBus):
    """
    Abstract base class for UART communication buses.

    Platform-specific UART backends should inherit from this class.
    """

    __slots__ = ()

    # ------------------------------------------------------------------
    # Device Communication
    # ------------------------------------------------------------------

    @abstractmethod
    def read(
        self,
        size: int = 1,
    ) -> bytes:
        """
        Read bytes from the UART.

        Parameters
        ----------
        size
            Number of bytes to read.

        Returns
        -------
        bytes
            Bytes read from the UART.
        """
        raise NotImplementedError

    @abstractmethod
    def readinto(
        self,
        buffer: bytearray,
    ) -> int:
        """
        Read bytes directly into an existing buffer.

        Parameters
        ----------
        buffer
            Destination buffer.

        Returns
        -------
        int
            Number of bytes read.
        """
        raise NotImplementedError

    @abstractmethod
    def write(
        self,
        data: bytes,
    ) -> int:
        """
        Write bytes to the UART.

        Parameters
        ----------
        data
            Bytes to transmit.

        Returns
        -------
        int
            Number of bytes written.
        """
        raise NotImplementedError

    @abstractmethod
    def writelines(
        self,
        lines: list[bytes],
    ) -> None:
        """
        Write multiple byte sequences.

        Parameters
        ----------
        lines
            List of byte sequences.
        """
        raise NotImplementedError

    @abstractmethod
    def flush(self) -> None:
        """
        Flush buffered output.
        """
        raise NotImplementedError

    @abstractmethod
    def reset_input_buffer(self) -> None:
        """
        Discard buffered input.
        """
        raise NotImplementedError

    @abstractmethod
    def reset_output_buffer(self) -> None:
        """
        Discard buffered output.
        """
        raise NotImplementedError
