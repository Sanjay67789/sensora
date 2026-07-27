"""
Native Linux UART backend for Sensora.
"""

from __future__ import annotations

from pathlib import Path
from types import TracebackType
from typing import Self

import serial

from sensora.buses.exceptions import (
    BusError,
    DeviceCommunicationError,
    InvalidDataError,
)
from sensora.buses.linux.base import LinuxBus


class LinuxUARTBus(LinuxBus):
    """
    Native Linux implementation of a UART communication bus.

    This backend communicates with Linux serial devices through
    the ``pyserial`` library.

    Parameters
    ----------
    device
        Linux serial device.

    baudrate
        UART baud rate.

    bytesize
        Number of data bits.

    parity
        UART parity.

    stopbits
        Number of stop bits.

    timeout
        Read timeout in seconds.
    """

    MIN_BAUDRATE = 50
    MAX_BAUDRATE = 4_000_000

    MIN_BYTESIZE = 5
    MAX_BYTESIZE = 8

    STOPBITS = (
        serial.STOPBITS_ONE,
        serial.STOPBITS_ONE_POINT_FIVE,
        serial.STOPBITS_TWO,
    )

    PARITY = (
        serial.PARITY_NONE,
        serial.PARITY_EVEN,
        serial.PARITY_ODD,
        serial.PARITY_MARK,
        serial.PARITY_SPACE,
    )

    __slots__ = (
        "_baudrate",
        "_bytesize",
        "_device",
        "_parity",
        "_serial",
        "_stopbits",
        "_timeout",
    )

    def __init__(
        self,
        device: str | Path = "/dev/ttyS0",
        baudrate: int = 115_200,
        *,
        bytesize: int = 8,
        parity: str = serial.PARITY_NONE,
        stopbits: float = serial.STOPBITS_ONE,
        timeout: float | None = 1.0,
    ) -> None:
        """
        Initialize the Linux UART backend.

        Parameters
        ----------
        device
            Linux serial device.

        baudrate
            UART baud rate.

        bytesize
            Number of data bits.

        parity
            UART parity.

        stopbits
            Number of stop bits.

        timeout
            Read timeout in seconds.
        """
        super().__init__()

        self._validate_device(device)
        self._validate_baudrate(baudrate)
        self._validate_bytesize(bytesize)
        self._validate_parity(parity)
        self._validate_stopbits(stopbits)
        self._validate_timeout(timeout)

        self._device = Path(device)
        self._baudrate = baudrate
        self._bytesize = bytesize
        self._parity = parity
        self._stopbits = stopbits
        self._timeout = timeout

        self._serial: serial.Serial | None = None

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def name(self) -> str:
        """Return the human-readable UART bus name."""
        return self._device.name

    @property
    def bus_type(self) -> str:
        """Return the communication bus type."""
        return "uart"

    @property
    def device(self) -> Path:
        """Return the Linux serial device."""
        return self._device

    # ------------------------------------------------------------------
    # Context Manager
    # ------------------------------------------------------------------

    def __enter__(self) -> Self:
        """
        Open the UART bus when entering a context manager.

        Returns
        -------
        Self
            Open UART bus instance.
        """
        self.open()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """
        Close the UART bus when leaving a context manager.
        """
        self.close()

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def open(self) -> None:
        """
        Open the Linux serial device.

        Raises
        ------
        BusAlreadyOpenError
            If the UART bus is already open.

        BusError
            If the serial device cannot be opened.
        """
        self._validate_closed()

        try:
            self.validate_device_path(self.device)

            uart = serial.Serial(
                port=str(self._device),
                baudrate=self._baudrate,
                bytesize=self._bytesize,
                parity=self._parity,
                stopbits=self._stopbits,
                timeout=self._timeout,
            )

            self._serial = uart
            self._set_open(True)

        except serial.SerialException as exc:
            self._serial = None

            raise BusError(f"Failed to open UART device '{self.device}'.") from exc

    def close(self) -> None:
        """
        Close the Linux serial device.

        Raises
        ------
        BusNotOpenError
            If the UART bus is not open.
        """
        self._validate_open()

        assert self._serial is not None

        try:
            self._serial.close()

        finally:
            self._serial = None
            self._set_open(False)

    # ------------------------------------------------------------------
    # Internal Helpers
    # ------------------------------------------------------------------

    def _require_bus(self) -> serial.Serial:
        """
        Return the active UART device.

        Returns
        -------
        serial.Serial
            Active UART device.

        Raises
        ------
        BusNotOpenError
            If the UART bus is not open.
        """
        self._validate_open()

        assert self._serial is not None

        return self._serial

    # ------------------------------------------------------------------
    # Communication
    # ------------------------------------------------------------------

    def write(
        self,
        data: bytes,
    ) -> int:
        """
        Write bytes to the UART device.

        Parameters
        ----------
        data
            Bytes to transmit.

        Returns
        -------
        int
            Number of bytes written.

        Raises
        ------
        DeviceCommunicationError
            If the write operation fails.

        InvalidDataError
            If the transmit buffer is invalid.
        """
        self._validate_transfer_data(data)

        uart = self._require_bus()

        try:
            bytes_written = uart.write(data)

            assert bytes_written is not None

            return bytes_written

        except serial.SerialException as exc:
            raise DeviceCommunicationError("UART write operation failed.") from exc

    def read(
        self,
        size: int,
    ) -> bytes:
        """
        Read bytes from the UART device.

        Parameters
        ----------
        size
            Number of bytes to read.

        Returns
        -------
        bytes
            Bytes received from the UART device.

        Raises
        ------
        DeviceCommunicationError
            If the read operation fails.

        InvalidDataError
            If the requested size is invalid.
        """
        self._validate_read_size(size)

        uart = self._require_bus()

        try:
            return uart.read(size)

        except serial.SerialException as exc:
            raise DeviceCommunicationError("UART read operation failed.") from exc

    def readinto(
        self,
        buffer: bytearray,
    ) -> int:
        """
        Read directly into a mutable buffer.

        Parameters
        ----------
        buffer
            Destination buffer.

        Returns
        -------
        int
            Number of bytes read.

        Raises
        ------
        DeviceCommunicationError
            If the read operation fails.

        InvalidDataError
            If the buffer is invalid.
        """
        self._validate_transfer_buffer(buffer)

        uart = self._require_bus()

        try:
            bytes_read = uart.readinto(buffer)
            assert bytes_read is not None
            return bytes_read
        except serial.SerialException as exc:
            raise DeviceCommunicationError("UART readinto operation failed.") from exc

    # ------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------

    @property
    def baudrate(self) -> int:
        """
        Return the configured baud rate.
        """
        return self._baudrate

    @baudrate.setter
    def baudrate(
        self,
        value: int,
    ) -> None:
        """
        Set the UART baud rate.

        Parameters
        ----------
        value
            UART baud rate.
        """
        self._validate_baudrate(value)

        self._baudrate = value

        if self.is_open:
            self._require_bus().baudrate = value

    @property
    def bytesize(self) -> int:
        """
        Return the configured byte size.
        """
        return self._bytesize

    @bytesize.setter
    def bytesize(
        self,
        value: int,
    ) -> None:
        """
        Set the UART byte size.

        Parameters
        ----------
        value
            Number of data bits.
        """
        self._validate_bytesize(value)

        self._bytesize = value

        if self.is_open:
            self._require_bus().bytesize = value

    @property
    def parity(self) -> str:
        """
        Return the configured parity.
        """
        return self._parity

    @parity.setter
    def parity(
        self,
        value: str,
    ) -> None:
        """
        Set the UART parity.

        Parameters
        ----------
        value
            UART parity.
        """
        self._validate_parity(value)

        self._parity = value

        if self.is_open:
            self._require_bus().parity = value

    @property
    def stopbits(self) -> float:
        """
        Return the configured stop bits.
        """
        return self._stopbits

    @stopbits.setter
    def stopbits(
        self,
        value: float,
    ) -> None:
        """
        Set the UART stop bits.

        Parameters
        ----------
        value
            Number of stop bits.
        """
        self._validate_stopbits(value)

        self._stopbits = value

        if self.is_open:
            self._require_bus().stopbits = value

    @property
    def timeout(self) -> float | None:
        """
        Return the configured read timeout.
        """
        return self._timeout

    @timeout.setter
    def timeout(
        self,
        value: float | None,
    ) -> None:
        """
        Set the UART read timeout.

        Parameters
        ----------
        value
            Read timeout in seconds.
        """
        self._validate_timeout(value)

        self._timeout = value

        if self.is_open:
            self._require_bus().timeout = value

    def configure(
        self,
        *,
        baudrate: int | None = None,
        bytesize: int | None = None,
        parity: str | None = None,
        stopbits: float | None = None,
        timeout: float | None = None,
    ) -> None:
        """
        Configure multiple UART parameters.

        Parameters
        ----------
        baudrate
            UART baud rate.

        bytesize
            Number of data bits.

        parity
            UART parity.

        stopbits
            Number of stop bits.

        timeout
            Read timeout in seconds.
        """
        if baudrate is not None:
            self.baudrate = baudrate

        if bytesize is not None:
            self.bytesize = bytesize

        if parity is not None:
            self.parity = parity

        if stopbits is not None:
            self.stopbits = stopbits

        if timeout is not None:
            self.timeout = timeout

    # ------------------------------------------------------------------
    # Advanced Communication
    # ------------------------------------------------------------------

    def read_until(
        self,
        expected: bytes = b"\n",
        size: int | None = None,
    ) -> bytes:
        """
        Read until the expected sequence is encountered.

        Parameters
        ----------
        expected
            Terminating byte sequence.

        size
            Maximum number of bytes to read.

        Returns
        -------
        bytes
            Bytes read from the UART device.

        Raises
        ------
        DeviceCommunicationError
            If the read operation fails.
        """
        uart = self._require_bus()

        try:
            return uart.read_until(expected=expected, size=size)

        except serial.SerialException as exc:
            raise DeviceCommunicationError("UART read_until operation failed.") from exc

    def readline(self) -> bytes:
        """
        Read a single line from the UART device.

        Returns
        -------
        bytes
            Line read from the UART device.
        """
        uart = self._require_bus()

        try:
            return uart.readline()

        except serial.SerialException as exc:
            raise DeviceCommunicationError("UART readline operation failed.") from exc

    def readlines(self) -> list[bytes]:
        """
        Read all available lines.

        Returns
        -------
        list[bytes]
            Lines read from the UART device.
        """
        uart = self._require_bus()

        try:
            return uart.readlines()

        except serial.SerialException as exc:
            raise DeviceCommunicationError("UART readlines operation failed.") from exc

    def writelines(
        self,
        lines: list[bytes],
    ) -> None:
        """
        Write multiple byte sequences.

        Parameters
        ----------
        lines
            Byte sequences to transmit.

        Raises
        ------
        DeviceCommunicationError
            If the write operation fails.
        """
        self._validate_lines(lines)

        uart = self._require_bus()

        try:
            uart.writelines(lines)

        except serial.SerialException as exc:
            raise DeviceCommunicationError("UART writelines operation failed.") from exc

    def flush(self) -> None:
        """
        Flush the UART output buffer.

        Raises
        ------
        DeviceCommunicationError
            If the flush operation fails.
        """
        uart = self._require_bus()

        try:
            uart.flush()

        except serial.SerialException as exc:
            raise DeviceCommunicationError("UART flush operation failed.") from exc

    def reset_input_buffer(self) -> None:
        """
        Clear the UART input buffer.

        Raises
        ------
        DeviceCommunicationError
            If the operation fails.
        """
        uart = self._require_bus()

        try:
            uart.reset_input_buffer()

        except serial.SerialException as exc:
            raise DeviceCommunicationError(
                "Failed to reset UART input buffer."
            ) from exc

    def reset_output_buffer(self) -> None:
        """
        Clear the UART output buffer.

        Raises
        ------
        DeviceCommunicationError
            If the operation fails.
        """
        uart = self._require_bus()

        try:
            uart.reset_output_buffer()

        except serial.SerialException as exc:
            raise DeviceCommunicationError(
                "Failed to reset UART output buffer."
            ) from exc

    def send_break(
        self,
        duration: float = 0.25,
    ) -> None:
        """
        Send a break condition.

        Parameters
        ----------
        duration
            Break duration in seconds.

        Raises
        ------
        DeviceCommunicationError
            If the operation fails.
        """
        uart = self._require_bus()

        try:
            uart.send_break(duration)

        except serial.SerialException as exc:
            raise DeviceCommunicationError("UART send_break operation failed.") from exc

    # ------------------------------------------------------------------
    # Modem Control & Status
    # ------------------------------------------------------------------

    @property
    def cts(self) -> bool:
        """
        Return the current Clear-To-Send (CTS) status.
        """
        return bool(self._require_bus().cts)

    @property
    def dsr(self) -> bool:
        """
        Return the current Data-Set-Ready (DSR) status.
        """
        return bool(self._require_bus().dsr)

    @property
    def ri(self) -> bool:
        """
        Return the current Ring Indicator (RI) status.
        """
        return bool(self._require_bus().ri)

    @property
    def cd(self) -> bool:
        """
        Return the current Carrier Detect (CD) status.
        """
        return bool(self._require_bus().cd)

    @property
    def rts(self) -> bool:
        """
        Return the current RTS state.
        """
        return bool(self._require_bus().rts)

    @rts.setter
    def rts(
        self,
        value: bool,
    ) -> None:
        """
        Set the RTS signal.

        Parameters
        ----------
        value
            Desired RTS state.
        """
        self._require_bus().rts = value

    @property
    def dtr(self) -> bool:
        """
        Return the current DTR state.
        """
        return bool(self._require_bus().dtr)

    @dtr.setter
    def dtr(
        self,
        value: bool,
    ) -> None:
        """
        Set the DTR signal.

        Parameters
        ----------
        value
            Desired DTR state.
        """
        self._require_bus().dtr = value

    @property
    def break_condition(self) -> bool:
        """
        Return whether break condition is active.
        """
        return bool(self._require_bus().break_condition)

    @break_condition.setter
    def break_condition(
        self,
        value: bool,
    ) -> None:
        """
        Enable or disable the break condition.

        Parameters
        ----------
        value
            Desired break state.
        """
        self._require_bus().break_condition = value

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    @classmethod
    def _validate_device(
        cls,
        device: str | Path,
    ) -> None:
        """
        Validate the UART device path.

        Parameters
        ----------
        device
            Linux serial device.

        Raises
        ------
        InvalidDataError
            If the device path is invalid.
        """
        if isinstance(device, str):
            device = Path(device)

        if not isinstance(device, Path):
            raise InvalidDataError("UART device must be a string or pathlib.Path.")

    @classmethod
    def _validate_baudrate(
        cls,
        baudrate: int,
    ) -> None:
        """
        Validate the UART baud rate.

        Parameters
        ----------
        baudrate
            UART baud rate.

        Raises
        ------
        InvalidDataError
            If the baud rate is invalid.
        """
        if not isinstance(baudrate, int):
            raise InvalidDataError("Baud rate must be an integer.")

        if not cls.MIN_BAUDRATE <= baudrate <= cls.MAX_BAUDRATE:
            raise InvalidDataError(
                f"Baud rate must be between "
                f"{cls.MIN_BAUDRATE} and {cls.MAX_BAUDRATE}."
            )

    @classmethod
    def _validate_bytesize(
        cls,
        bytesize: int,
    ) -> None:
        """
        Validate the UART byte size.

        Parameters
        ----------
        bytesize
            Number of data bits.

        Raises
        ------
        InvalidDataError
            If the byte size is invalid.
        """
        if not isinstance(bytesize, int):
            raise InvalidDataError("Byte size must be an integer.")

        if not cls.MIN_BYTESIZE <= bytesize <= cls.MAX_BYTESIZE:
            raise InvalidDataError(
                f"Byte size must be between "
                f"{cls.MIN_BYTESIZE} and {cls.MAX_BYTESIZE}."
            )

    @classmethod
    def _validate_parity(
        cls,
        parity: str,
    ) -> None:
        """
        Validate the UART parity.

        Parameters
        ----------
        parity
            UART parity.

        Raises
        ------
        InvalidDataError
            If the parity is invalid.
        """
        if parity not in cls.PARITY:
            raise InvalidDataError("Invalid UART parity.")

    @classmethod
    def _validate_stopbits(
        cls,
        stopbits: float,
    ) -> None:
        """
        Validate the UART stop bits.

        Parameters
        ----------
        stopbits
            Number of stop bits.

        Raises
        ------
        InvalidDataError
            If the stop bits are invalid.
        """
        if stopbits not in cls.STOPBITS:
            raise InvalidDataError("Invalid UART stop bits.")

    @classmethod
    def _validate_timeout(
        cls,
        timeout: float | None,
    ) -> None:
        """
        Validate the UART timeout.

        Parameters
        ----------
        timeout
            Read timeout.

        Raises
        ------
        InvalidDataError
            If the timeout is invalid.
        """
        if timeout is None:
            return

        if not isinstance(timeout, (int, float)):
            raise InvalidDataError("Timeout must be a number or None.")

        if timeout < 0:
            raise InvalidDataError("Timeout cannot be negative.")

    @classmethod
    def _validate_transfer_data(
        cls,
        data: bytes,
    ) -> None:
        """
        Validate transmit data.

        Parameters
        ----------
        data
            Bytes to transmit.

        Raises
        ------
        InvalidDataError
            If the transmit buffer is invalid.
        """
        if not isinstance(data, bytes):
            raise InvalidDataError("Transfer data must be bytes.")

        if len(data) == 0:
            raise InvalidDataError("Transfer buffer cannot be empty.")

    @classmethod
    def _validate_transfer_buffer(
        cls,
        buffer: bytearray,
    ) -> None:
        """
        Validate a mutable buffer.

        Parameters
        ----------
        buffer
            Destination buffer.

        Raises
        ------
        InvalidDataError
            If the buffer is invalid.
        """
        if not isinstance(buffer, bytearray):
            raise InvalidDataError("Buffer must be a bytearray.")

        if len(buffer) == 0:
            raise InvalidDataError("Buffer cannot be empty.")

    @classmethod
    def _validate_read_size(
        cls,
        size: int,
    ) -> None:
        """
        Validate the read size.

        Parameters
        ----------
        size
            Number of bytes to read.

        Raises
        ------
        InvalidDataError
            If the read size is invalid.
        """
        if not isinstance(size, int):
            raise InvalidDataError("Read size must be an integer.")

        if size <= 0:
            raise InvalidDataError("Read size must be greater than zero.")

    @classmethod
    def _validate_lines(
        cls,
        lines: list[bytes],
    ) -> None:
        """
        Validate a list of byte sequences.

        Parameters
        ----------
        lines
            Byte sequences to write.

        Raises
        ------
        InvalidDataError
            If the sequence is invalid.
        """
        if not isinstance(lines, list):
            raise InvalidDataError("Lines must be a list.")

        for line in lines:
            cls._validate_transfer_data(line)

    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------

    @property
    def configuration(self) -> dict[str, object]:
        """
        Return the current UART configuration.

        Returns
        -------
        dict[str, object]
            Current UART configuration.
        """
        return {
            "device": str(self._device),
            "baudrate": self._baudrate,
            "bytesize": self._bytesize,
            "parity": self._parity,
            "stopbits": self._stopbits,
            "timeout": self._timeout,
        }

    @property
    def device_name(self) -> str:
        """
        Return the Linux UART device name.

        Returns
        -------
        str
            Linux device path.
        """
        return str(self.device)

    def __repr__(self) -> str:
        """
        Return the developer representation.

        Returns
        -------
        str
            Representation string.
        """
        return (
            f"{self.__class__.__name__}("
            f"device={self._device!s}, "
            f"baudrate={self._baudrate}, "
            f"bytesize={self._bytesize}, "
            f"parity={self._parity!r}, "
            f"stopbits={self._stopbits}, "
            f"timeout={self._timeout}, "
            f"is_open={self.is_open})"
        )

    def __str__(self) -> str:
        """
        Return a human-readable description.

        Returns
        -------
        str
            Description string.
        """
        return f"UART({self.device}) " f"[{self._baudrate} baud]"

    def __eq__(
        self,
        other: object,
    ) -> bool:
        """
        Compare two UART buses.

        Parameters
        ----------
        other
            Object to compare.

        Returns
        -------
        bool
            True if both buses refer to the same device.
        """
        if not isinstance(other, LinuxUARTBus):
            return NotImplemented

        return self._device == other._device

    def __hash__(self) -> int:
        """
        Return the hash value.

        Returns
        -------
        int
            Hash value.
        """
        return hash(self._device)

    def reopen(self) -> None:
        """
        Reopen the UART device.
        """
        self.reset()

    def info(self) -> dict[str, object]:
        """
        Return information about the UART device.

        Returns
        -------
        dict[str, object]
            UART device information.
        """
        return {
            "name": self.name,
            "bus_type": self.bus_type,
            "device": str(self.device),
            "is_open": self.is_open,
            "configuration": self.configuration,
        }
