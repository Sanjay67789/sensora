"""
Native Linux SPI backend for Sensora.
"""

from __future__ import annotations

from pathlib import Path
from types import TracebackType
from typing import Self

import spidev

from sensora.buses.exceptions import (
    BusError,
    DeviceCommunicationError,
    InvalidDataError,
)
from sensora.buses.linux.base import LinuxBus
from sensora.buses.spi import SPIBus


class LinuxSPIBus(LinuxBus, SPIBus):
    """
    Native Linux implementation of an SPI communication bus.

    This backend communicates with Linux ``spidev`` devices through
    the ``spidev`` library.

    Parameters
    ----------
    bus
        Linux SPI bus number.

    chip_select
        Chip select (CS) line.

    max_speed_hz
        SPI clock frequency in Hertz.

    mode
        SPI mode (0-3).

    bits_per_word
        Number of bits transferred per word.
    """

    MIN_BUS = 0

    MIN_CHIP_SELECT = 0

    MIN_SPEED_HZ = 1
    MAX_SPEED_HZ = 125_000_000

    MIN_BITS_PER_WORD = 8
    MAX_BITS_PER_WORD = 16

    MIN_MODE = 0
    MAX_MODE = 3

    __slots__ = (
        "_bits_per_word",
        "_bus",
        "_chip_select",
        "_max_speed_hz",
        "_mode",
        "_spi",
    )

    def __init__(
        self,
        bus: int = 0,
        chip_select: int = 0,
        max_speed_hz: int = 1_000_000,
        mode: int = 0,
        bits_per_word: int = 8,
    ) -> None:
        """
        Initialize the Linux SPI backend.

        Parameters
        ----------
        bus
            Linux SPI bus number.

        chip_select
            Chip select line.

        max_speed_hz
            SPI clock frequency in Hertz.

        mode
            SPI mode (0-3).

        bits_per_word
            Number of bits transferred per word.
        """
        super().__init__()

        self._validate_bus(bus)
        self._validate_chip_select(chip_select)
        self._validate_speed(max_speed_hz)
        self._validate_mode(mode)
        self._validate_bits_per_word(bits_per_word)

        self._bus = bus
        self._chip_select = chip_select
        self._max_speed_hz = max_speed_hz
        self._mode = mode
        self._bits_per_word = bits_per_word

        self._spi: spidev.SpiDev | None = None

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def name(self) -> str:
        """Return the human-readable SPI bus name."""
        return f"SPI-{self._bus}.{self._chip_select}"

    @property
    def bus_type(self) -> str:
        """Return the communication bus type."""
        return "spi"

    @property
    def bus(self) -> int:
        """Return the Linux SPI bus number."""
        return self._bus

    @property
    def chip_select(self) -> int:
        """Return the chip select line."""
        return self._chip_select

    @property
    def device(self) -> Path:
        """Return the Linux SPI device node."""
        return Path(f"/dev/spidev{self._bus}.{self._chip_select}")

    # ------------------------------------------------------------------
    # Context Manager
    # ------------------------------------------------------------------

    def __enter__(self) -> Self:
        """
        Open the SPI bus when entering a context manager.

        Returns
        -------
        Self
            Open SPI bus instance.
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
        Close the SPI bus when leaving a context manager.
        """
        self.close()

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def open(self) -> None:
        """
        Open the Linux SPI device.

        Raises
        ------
        BusAlreadyOpenError
            If the SPI bus is already open.

        BusError
            If the SPI device cannot be opened.
        """
        self._validate_closed()

        try:
            self.validate_device_path(self.device)

            spi = spidev.SpiDev()
            spi.open(
                self._bus,
                self._chip_select,
            )

            spi.max_speed_hz = self._max_speed_hz
            spi.mode = self._mode
            spi.bits_per_word = self._bits_per_word

            self._spi = spi
            self._set_open(True)

        except OSError as exc:
            self._spi = None
            raise BusError(f"Failed to open SPI bus '{self.device}'.") from exc

    def close(self) -> None:
        """
        Close the Linux SPI device.

        Raises
        ------
        BusNotOpenError
            If the SPI bus has not been opened.
        """
        self._validate_open()

        assert self._spi is not None

        try:
            self._spi.close()

        finally:
            self._spi = None
            self._set_open(False)

    # ------------------------------------------------------------------
    # Internal Helpers
    # ------------------------------------------------------------------

    def _require_bus(self) -> spidev.SpiDev:
        """
        Return the active SPI device.

        Returns
        -------
        spidev.SpiDev
            Active SPI device.

        Raises
        ------
        BusNotOpenError
            If the SPI bus is not open.
        """
        self._validate_open()

        assert self._spi is not None

        return self._spi

    # ------------------------------------------------------------------
    # Communication
    # ------------------------------------------------------------------

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
            Bytes received from the SPI device.

        Raises
        ------
        DeviceCommunicationError
            If the SPI transfer fails.

        InvalidDataError
            If the transmit buffer is invalid.
        """
        self._validate_transfer_data(data)

        spi = self._require_bus()

        try:
            response = spi.xfer2(list(data))
            return bytes(response)

        except OSError as exc:
            raise DeviceCommunicationError("SPI transfer failed.") from exc

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

        Raises
        ------
        DeviceCommunicationError
            If the write operation fails.

        InvalidDataError
            If the transmit buffer is invalid.
        """
        self._validate_transfer_data(data)

        spi = self._require_bus()

        try:
            spi.xfer2(list(data))

        except OSError as exc:
            raise DeviceCommunicationError("SPI write operation failed.") from exc

    def read(
        self,
        length: int,
    ) -> bytes:
        """
        Read bytes from the SPI device.

        The SPI master transmits dummy bytes (0x00) while reading.

        Parameters
        ----------
        length
            Number of bytes to read.

        Returns
        -------
        bytes
            Bytes received from the SPI device.

        Raises
        ------
        DeviceCommunicationError
            If the read operation fails.

        InvalidDataError
            If the requested length is invalid.
        """
        self._validate_read_length(length)

        spi = self._require_bus()

        try:
            response = spi.xfer2([0] * length)
            return bytes(response)

        except OSError as exc:
            raise DeviceCommunicationError("SPI read operation failed.") from exc

    def transfer_in_place(
        self,
        buffer: bytearray,
    ) -> None:
        """
        Perform an in-place SPI transfer.

        The supplied buffer is overwritten with the received bytes.

        Parameters
        ----------
        buffer
            Mutable transfer buffer.

        Raises
        ------
        DeviceCommunicationError
            If the SPI transfer fails.

        InvalidDataError
            If the buffer is invalid.
        """
        self._validate_transfer_buffer(buffer)

        spi = self._require_bus()

        try:
            response = spi.xfer2(list(buffer))
            buffer[:] = response

        except OSError as exc:
            raise DeviceCommunicationError("SPI transfer failed.") from exc

    # ------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------

    @property
    def max_speed_hz(self) -> int:
        """
        Maximum SPI clock frequency in Hertz.
        """
        return self._max_speed_hz

    @max_speed_hz.setter
    def max_speed_hz(
        self,
        value: int,
    ) -> None:
        """
        Set the SPI clock frequency.

        Parameters
        ----------
        value
            Clock frequency in Hertz.
        """
        self._validate_speed(value)

        self._max_speed_hz = value

        if self.is_open:
            self._require_bus().max_speed_hz = value

    @property
    def mode(self) -> int:
        """
        SPI mode.
        """
        return self._mode

    @mode.setter
    def mode(
        self,
        value: int,
    ) -> None:
        """
        Set the SPI mode.

        Parameters
        ----------
        value
            SPI mode (0-3).
        """
        self._validate_mode(value)

        self._mode = value

        if self.is_open:
            self._require_bus().mode = value

    @property
    def bits_per_word(self) -> int:
        """
        Number of bits per SPI word.
        """
        return self._bits_per_word

    @bits_per_word.setter
    def bits_per_word(
        self,
        value: int,
    ) -> None:
        """
        Set the SPI word size.

        Parameters
        ----------
        value
            Number of bits per word.
        """
        self._validate_bits_per_word(value)

        self._bits_per_word = value

        if self.is_open:
            self._require_bus().bits_per_word = value

    @property
    def lsb_first(self) -> bool:
        """
        Whether LSB-first transmission is enabled.
        """
        spi = self._require_bus()
        return bool(spi.lsbfirst)

    @lsb_first.setter
    def lsb_first(
        self,
        value: bool,
    ) -> None:
        """
        Enable or disable LSB-first transmission.
        """
        spi = self._require_bus()
        spi.lsbfirst = value

    @property
    def cshigh(self) -> bool:
        """
        Whether chip-select is active-high.
        """
        spi = self._require_bus()
        return bool(spi.cshigh)

    @cshigh.setter
    def cshigh(
        self,
        value: bool,
    ) -> None:
        """
        Configure chip-select polarity.
        """
        spi = self._require_bus()
        spi.cshigh = value

    @property
    def threewire(self) -> bool:
        """
        Whether three-wire SPI mode is enabled.
        """
        spi = self._require_bus()
        return bool(spi.threewire)

    @threewire.setter
    def threewire(
        self,
        value: bool,
    ) -> None:
        """
        Enable or disable three-wire SPI mode.
        """
        spi = self._require_bus()
        spi.threewire = value

    @property
    def loop(self) -> bool:
        """
        Whether SPI loopback mode is enabled.
        """
        spi = self._require_bus()
        return bool(spi.loop)

    @loop.setter
    def loop(
        self,
        value: bool,
    ) -> None:
        """
        Enable or disable loopback mode.
        """
        spi = self._require_bus()
        spi.loop = value

    def configure(
        self,
        *,
        max_speed_hz: int | None = None,
        mode: int | None = None,
        bits_per_word: int | None = None,
    ) -> None:
        """
        Configure multiple SPI parameters.

        Parameters
        ----------
        max_speed_hz
            SPI clock frequency.

        mode
            SPI mode (0-3).

        bits_per_word
            Bits per transfer word.
        """
        if max_speed_hz is not None:
            self.max_speed_hz = max_speed_hz

        if mode is not None:
            self.mode = mode

        if bits_per_word is not None:
            self.bits_per_word = bits_per_word

    # ------------------------------------------------------------------
    # Advanced Communication
    # ------------------------------------------------------------------

    def transfer_words(
        self,
        data: list[int],
    ) -> list[int]:
        """
        Perform a full-duplex SPI transfer using word values.

        Parameters
        ----------
        data
            Sequence of integer values to transmit.

        Returns
        -------
        list[int]
            Values received from the SPI device.

        Raises
        ------
        DeviceCommunicationError
            If the transfer fails.

        InvalidDataError
            If the transmit data is invalid.
        """
        self._validate_word_transfer_data(data)

        spi = self._require_bus()

        try:
            return spi.xfer2(data)

        except OSError as exc:
            raise DeviceCommunicationError("SPI transfer failed.") from exc

    def write_word(
        self,
        value: int,
    ) -> None:
        """
        Write a single SPI word.

        Parameters
        ----------
        value
            Word value to transmit.
        """
        self.transfer_words([value])

    def read_word(self) -> int:
        """
        Read a single SPI word.

        Returns
        -------
        int
            Word received from the SPI device.
        """
        return self.transfer_words([0])[0]

    def transfer_byte(
        self,
        value: int,
    ) -> int:
        """
        Transfer a single byte.

        Parameters
        ----------
        value
            Byte to transmit.

        Returns
        -------
        int
            Byte received.
        """
        self._validate_byte(value)

        return self.transfer_words([value])[0]

    def write_byte(
        self,
        value: int,
    ) -> None:
        """
        Write a single byte.
        """
        self.transfer_byte(value)

    def read_byte(self) -> int:
        """
        Read a single byte.

        Returns
        -------
        int
            Byte received.
        """
        return self.transfer_byte(0x00)

    def transfer_memoryview(
        self,
        buffer: memoryview,
    ) -> bytes:
        """
        Perform a transfer using a memoryview.

        Parameters
        ----------
        buffer
            Buffer to transmit.

        Returns
        -------
        bytes
            Received bytes.
        """
        return self.transfer(buffer.tobytes())

    def write_memoryview(
        self,
        buffer: memoryview,
    ) -> None:
        """
        Write a memoryview.
        """
        self.write(buffer.tobytes())

    def readinto(
        self,
        buffer: bytearray,
    ) -> None:
        """
        Read directly into a bytearray.

        Parameters
        ----------
        buffer
            Destination buffer.
        """
        buffer[:] = self.read(len(buffer))

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    @classmethod
    def _validate_bus(
        cls,
        bus: int,
    ) -> None:
        """
        Validate the SPI bus number.

        Parameters
        ----------
        bus
            SPI bus number.

        Raises
        ------
        InvalidDataError
            If the bus number is invalid.
        """
        if bus < cls.MIN_BUS:
            raise InvalidDataError("SPI bus number must be non-negative.")

    @classmethod
    def _validate_chip_select(
        cls,
        chip_select: int,
    ) -> None:
        """
        Validate the chip-select number.

        Parameters
        ----------
        chip_select
            Chip-select number.

        Raises
        ------
        InvalidDataError
            If the chip-select number is invalid.
        """
        if chip_select < cls.MIN_CHIP_SELECT:
            raise InvalidDataError("Chip-select number must be non-negative.")

    @classmethod
    def _validate_speed(
        cls,
        speed: int,
    ) -> None:
        """
        Validate the SPI clock speed.

        Parameters
        ----------
        speed
            Clock speed in Hertz.

        Raises
        ------
        InvalidDataError
            If the speed is invalid.
        """
        if not isinstance(speed, int):
            raise InvalidDataError("SPI clock speed must be an integer.")

        if speed < cls.MIN_SPEED_HZ:
            raise InvalidDataError("SPI clock speed must be greater than zero.")

    @classmethod
    def _validate_mode(
        cls,
        mode: int,
    ) -> None:
        """
        Validate the SPI mode.

        Parameters
        ----------
        mode
            SPI mode.

        Raises
        ------
        InvalidDataError
            If the mode is invalid.
        """
        if mode not in (0, 1, 2, 3):
            raise InvalidDataError("SPI mode must be between 0 and 3.")

    @classmethod
    def _validate_bits_per_word(
        cls,
        bits: int,
    ) -> None:
        """
        Validate the SPI word size.

        Parameters
        ----------
        bits
            Number of bits per SPI word.

        Raises
        ------
        InvalidDataError
            If the word size is invalid.
        """
        if not isinstance(bits, int):
            raise InvalidDataError("Bits per word must be an integer.")

        if bits < cls.MIN_BITS_PER_WORD:
            raise InvalidDataError("Bits per word must be at least 8.")

        if bits > cls.MAX_BITS_PER_WORD:
            raise InvalidDataError("Bits per word cannot exceed 16.")

    @classmethod
    def _validate_transfer_data(
        cls,
        data: bytes,
    ) -> None:
        """
        Validate a transfer buffer.

        Parameters
        ----------
        data
            Transfer buffer.

        Raises
        ------
        InvalidDataError
            If the transfer buffer is invalid.
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
        Validate an in-place transfer buffer.

        Parameters
        ----------
        buffer
            Transfer buffer.

        Raises
        ------
        InvalidDataError
            If the buffer is invalid.
        """
        if not isinstance(buffer, bytearray):
            raise InvalidDataError("Transfer buffer must be a bytearray.")

        if len(buffer) == 0:
            raise InvalidDataError("Transfer buffer cannot be empty.")

    @classmethod
    def _validate_read_length(
        cls,
        length: int,
    ) -> None:
        """
        Validate a read length.

        Parameters
        ----------
        length
            Number of bytes to read.

        Raises
        ------
        InvalidDataError
            If the length is invalid.
        """
        if not isinstance(length, int):
            raise InvalidDataError("Read length must be an integer.")

        if length <= 0:
            raise InvalidDataError("Read length must be greater than zero.")

    @classmethod
    def _validate_byte(
        cls,
        value: int,
    ) -> None:
        """
        Validate an SPI byte.

        Parameters
        ----------
        value
            Byte value.

        Raises
        ------
        InvalidDataError
            If the value is invalid.
        """
        if not isinstance(value, int):
            raise InvalidDataError("SPI byte must be an integer.")

        if not 0 <= value <= 0xFF:
            raise InvalidDataError("SPI byte must be between 0x00 and 0xFF.")

    @classmethod
    def _validate_word_transfer_data(
        cls,
        data: list[int],
    ) -> None:
        """
        Validate a word transfer buffer.

        Parameters
        ----------
        data
            Transfer values.

        Raises
        ------
        InvalidDataError
            If the transfer values are invalid.
        """
        if not data:
            raise InvalidDataError("Transfer buffer cannot be empty.")

        for value in data:
            cls._validate_byte(value)

    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------

    @property
    def configuration(self) -> dict[str, int]:
        """
        Return the current SPI configuration.

        Returns
        -------
        dict[str, int]
            Current SPI configuration.
        """
        return {
            "bus": self._bus,
            "chip_select": self._chip_select,
            "max_speed_hz": self._max_speed_hz,
            "mode": self._mode,
            "bits_per_word": self._bits_per_word,
        }

    @property
    def device_name(self) -> str:
        """
        Return the Linux SPI device name.

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
            f"bus={self._bus}, "
            f"chip_select={self._chip_select}, "
            f"max_speed_hz={self._max_speed_hz}, "
            f"mode={self._mode}, "
            f"bits_per_word={self._bits_per_word}, "
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
        return (
            f"SPI({self.device}) " f"[mode={self._mode}, " f"{self._max_speed_hz} Hz]"
        )

    def __eq__(
        self,
        other: object,
    ) -> bool:
        """
        Compare two SPI buses.

        Parameters
        ----------
        other
            Object to compare.

        Returns
        -------
        bool
            True if both buses refer to the same device.
        """
        if not isinstance(other, LinuxSPIBus):
            return NotImplemented

        return self._bus == other._bus and self._chip_select == other._chip_select

    def __hash__(self) -> int:
        """
        Return the hash value.

        Returns
        -------
        int
            Hash value.
        """
        return hash(
            (
                self._bus,
                self._chip_select,
            )
        )

    def reopen(self) -> None:
        """
        Reopen the SPI device.
        """
        self.reset()

    def info(self) -> dict[str, object]:
        """
        Return information about the SPI device.

        Returns
        -------
        dict[str, object]
            SPI device information.
        """
        return {
            "name": self.name,
            "bus_type": self.bus_type,
            "device": str(self.device),
            "is_open": self.is_open,
            "configuration": self.configuration,
        }
