"""
Native Linux I²C backend for Sensora.
"""

from __future__ import annotations

from pathlib import Path
from types import TracebackType
from typing import Self

from smbus2 import SMBus, i2c_msg

from sensora.buses.exceptions import (
    BusError,
    BusScanError,
    DeviceCommunicationError,
    InvalidAddressError,
    InvalidDataError,
    InvalidRegisterError,
)
from sensora.buses.linux.base import LinuxBus


class LinuxI2CBus(LinuxBus):
    """
    Native Linux implementation of an I²C communication bus.

    This backend communicates with Linux ``i2c-dev`` devices through
    the ``smbus2`` library.

    Parameters
    ----------
    bus_id
        Linux I²C adapter number (for example ``1`` for
        ``/dev/i2c-1``).
    """

    MIN_ADDRESS = 0x03
    MAX_ADDRESS = 0x77
    MIN_REGISTER = 0x00
    MAX_REGISTER = 0xFF
    MIN_BYTE = 0x00
    MAX_BYTE = 0xFF

    __slots__ = (
        "_bus",
        "_bus_id",
    )

    def __init__(self, bus_id: int = 1) -> None:
        """
        Initialize the Linux I²C backend.

        Parameters
        ----------
        bus_id
            Linux I²C adapter number.
        """
        super().__init__()

        self._bus_id = bus_id
        self._bus: SMBus | None = None

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def name(self) -> str:
        """Return the human-readable bus name."""
        return f"I2C-{self._bus_id}"

    @property
    def bus_type(self) -> str:
        """Return the communication bus type."""
        return "i2c"

    @property
    def bus_id(self) -> int:
        """Return the Linux adapter number."""
        return self._bus_id

    @property
    def device(self) -> Path:
        """Return the Linux device node."""
        return Path(f"/dev/i2c-{self._bus_id}")

    # ------------------------------------------------------------------
    # Context manager
    # ------------------------------------------------------------------

    def __enter__(self) -> Self:
        self.open()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def open(self) -> None:
        """
        Open the Linux I²C device.

        Raises
        ------
        BusAlreadyOpenError
            If the bus is already open.

        BusError
            If the device cannot be opened.
        """
        self._validate_closed()

        try:
            self.validate_device_path(self.device)

            self._bus = SMBus(self._bus_id)

            self._set_open(True)

        except Exception as exc:
            self._bus = None
            raise BusError(f"Failed to open I²C bus '{self.device}'.") from exc

    def close(self) -> None:
        """
        Close the Linux I²C device.

        Raises
        ------
        BusNotOpenError
            If the bus has not been opened.
        """
        self._validate_open()

        assert self._bus is not None

        try:
            self._bus.close()

        finally:
            self._bus = None
            self._set_open(False)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _require_bus(self) -> SMBus:
        """
        Return the active SMBus instance.

        Returns
        -------
        SMBus
            Open SMBus object.

        Raises
        ------
        BusNotOpenError
            If the bus is not open.
        """
        self._validate_open()

        assert self._bus is not None

        return self._bus

    # ------------------------------------------------------------------
    # Discovery
    # ------------------------------------------------------------------

    def ping(self, address: int) -> bool:
        """
        Check whether a device responds at the given address.

        Parameters
        ----------
        address
            7-bit I²C device address.

        Returns
        -------
        bool
            True if the device acknowledges, otherwise False.
        """
        self._validate_address(address)

        try:
            self.read_byte(address)
            return True

        except DeviceCommunicationError:
            return False

    def scan(self) -> list[int]:
        """
        Scan the I²C bus for responding devices.

        Returns
        -------
        list[int]
            List of detected 7-bit device addresses.

        Raises
        ------
        BusScanError
            If the scan cannot be completed.
        """
        bus = self._require_bus()

        devices: list[int] = []

        try:
            for address in range(
                self.MIN_ADDRESS,
                self.MAX_ADDRESS + 1,
            ):
                try:
                    bus.read_byte(address)
                    devices.append(address)

                except OSError:
                    continue

            return devices

        except Exception as exc:
            raise BusScanError(f"Failed to scan '{self.device}'.") from exc

    # ------------------------------------------------------------------
    # Communication
    # ------------------------------------------------------------------

    def read_byte(self, address: int) -> int:
        """
        Read a single byte from an I²C device.

        Parameters
        ----------
        address
            7-bit I²C device address.

        Returns
        -------
        int
            Value read from the device.
        """
        self._validate_address(address)

        bus = self._require_bus()

        try:
            return bus.read_byte(address)

        except OSError as exc:
            raise DeviceCommunicationError(
                f"Failed to read byte from device " f"0x{address:02X}."
            ) from exc

    def write_byte(
        self,
        address: int,
        value: int,
    ) -> None:
        """
        Write a single byte to an I²C device.

        Parameters
        ----------
        address
            7-bit I²C device address.

        value
            Byte to write.
        """
        self._validate_address(address)
        self._validate_byte(value)

        bus = self._require_bus()

        try:
            bus.write_byte(address, value)

        except OSError as exc:
            raise DeviceCommunicationError(
                f"Failed to write byte to device " f"0x{address:02X}."
            ) from exc

    def read_word(
        self,
        address: int,
        register: int,
    ) -> int:
        """
        Read a 16-bit word from a device register.
        """
        self._validate_address(address)
        self._validate_register(register)

        bus = self._require_bus()

        try:
            return bus.read_word_data(
                address,
                register,
            )

        except OSError as exc:
            raise DeviceCommunicationError(
                f"Failed to read word from register " f"0x{register:02X}."
            ) from exc

    def write_word(
        self,
        address: int,
        register: int,
        value: int,
    ) -> None:
        """
        Write a 16-bit word to a device register.
        """
        self._validate_address(address)
        self._validate_register(register)

        if not 0 <= value <= 0xFFFF:
            raise InvalidDataError("Word value must be between " "0x0000 and 0xFFFF.")

        bus = self._require_bus()

        try:
            bus.write_word_data(
                address,
                register,
                value,
            )

        except OSError as exc:
            raise DeviceCommunicationError(
                f"Failed to write word to register " f"0x{register:02X}."
            ) from exc

    def read_register(
        self,
        address: int,
        register: int,
    ) -> int:
        """
        Read one byte from a register.
        """
        self._validate_address(address)
        self._validate_register(register)

        bus = self._require_bus()

        try:
            return bus.read_byte_data(
                address,
                register,
            )

        except OSError as exc:
            raise DeviceCommunicationError(
                f"Failed to read register " f"0x{register:02X}."
            ) from exc

    def write_register(
        self,
        address: int,
        register: int,
        value: int,
    ) -> None:
        """
        Write one byte to a register.
        """
        self._validate_address(address)
        self._validate_register(register)
        self._validate_byte(value)

        bus = self._require_bus()

        try:
            bus.write_byte_data(
                address,
                register,
                value,
            )

        except OSError as exc:
            raise DeviceCommunicationError(
                f"Failed to write register " f"0x{register:02X}."
            ) from exc

    def read_block(
        self,
        address: int,
        register: int,
        length: int,
    ) -> list[int]:
        """
        Read a block of bytes from a device register.

        Parameters
        ----------
        address
            7-bit I²C device address.

        register
            Register address.

        length
            Number of bytes to read.

        Returns
        -------
        list[int]
            Bytes read from the device.
        """
        self._validate_address(address)
        self._validate_register(register)

        if length <= 0:
            raise InvalidDataError("Block length must be greater than zero.")

        bus = self._require_bus()

        try:
            return bus.read_i2c_block_data(
                address,
                register,
                length,
            )

        except OSError as exc:
            raise DeviceCommunicationError("Failed to read data block.") from exc

    def write_block(
        self,
        address: int,
        register: int,
        data: list[int],
    ) -> None:
        """
        Write a block of bytes to a device register.

        Parameters
        ----------
        address
            7-bit I²C device address.

        register
            Register address.

        data
            Sequence of bytes to write.
        """
        self._validate_address(address)
        self._validate_register(register)

        if not data:
            raise InvalidDataError("Data block cannot be empty.")

        for value in data:
            self._validate_byte(value)

        bus = self._require_bus()

        try:
            bus.write_i2c_block_data(
                address,
                register,
                data,
            )

        except OSError as exc:
            raise DeviceCommunicationError("Failed to write data block.") from exc

    def transfer(
        self,
        address: int,
        write: bytes = b"",
        read_length: int = 0,
    ) -> bytes:
        """
        Perform a raw I²C transaction.

        Parameters
        ----------
        address
            7-bit I²C device address.

        write
            Bytes written before the read.

        read_length
            Number of bytes to read.

        Returns
        -------
        bytes
            Bytes returned by the device.
        """
        self._validate_address(address)

        if read_length < 0:
            raise InvalidDataError("read_length cannot be negative.")

        bus = self._require_bus()

        try:
            messages = []

            if write:
                messages.append(
                    i2c_msg.write(
                        address,
                        write,
                    )
                )

            if read_length:
                read_msg = i2c_msg.read(
                    address,
                    read_length,
                )

                messages.append(read_msg)

            bus.i2c_rdwr(*messages)

            if read_length:
                return bytes(read_msg)

            return b""

        except OSError as exc:
            raise DeviceCommunicationError("Raw I²C transaction failed.") from exc

    # ------------------------------------------------------------------
    # Validation helpers
    # ------------------------------------------------------------------

    @classmethod
    def _validate_address(
        cls,
        address: int,
    ) -> None:
        """
        Validate a 7-bit I²C device address.

        Parameters
        ----------
        address
            Device address.

        Raises
        ------
        InvalidAddressError
            If the address is outside the valid range.
        """
        if not isinstance(address, int):
            raise InvalidAddressError("I²C address must be an integer.")

        if not cls.MIN_ADDRESS <= address <= cls.MAX_ADDRESS:
            raise InvalidAddressError(f"Invalid I²C address: 0x{address:02X}.")

    @classmethod
    def _validate_register(
        cls,
        register: int,
    ) -> None:
        """
        Validate an 8-bit register address.

        Parameters
        ----------
        register
            Register address.

        Raises
        ------
        InvalidRegisterError
            If the register is outside the valid range.
        """
        if not isinstance(register, int):
            raise InvalidRegisterError("Register must be an integer.")

        if not cls.MIN_REGISTER <= register <= cls.MAX_REGISTER:
            raise InvalidRegisterError(f"Invalid register: 0x{register:02X}.")

    @classmethod
    def _validate_byte(
        cls,
        value: int,
    ) -> None:
        """
        Validate an 8-bit value.

        Parameters
        ----------
        value
            Byte value.

        Raises
        ------
        InvalidDataError
            If the value is outside the valid range.
        """
        if not isinstance(value, int):
            raise InvalidDataError("Byte value must be an integer.")

        if not cls.MIN_BYTE <= value <= cls.MAX_BYTE:
            raise InvalidDataError(f"Invalid byte value: {value}.")
