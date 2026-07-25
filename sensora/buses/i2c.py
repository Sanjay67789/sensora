"""I²C bus implementation for Sensora."""

from __future__ import annotations

from smbus2 import SMBus

from sensora.buses.base import BaseBus
from sensora.core.exceptions import (
    BusError,
    DeviceCommunicationError,
)


class I2CBus(BaseBus):
    """
    Linux I²C bus implementation.

    This class provides low-level communication primitives for I²C devices.
    Device discovery and driver logic are intentionally implemented in
    higher layers of the framework.
    """

    def __init__(self, bus_id: int = 1) -> None:
        """
        Initialize an I²C bus.

        Args:
            bus_id:
                Linux I²C bus number (default: 1).
        """
        self._bus_id = bus_id
        self._bus: SMBus | None = None

    def open(self) -> None:
        """
        Open the I²C bus.

        Raises:
            BusError:
                If the bus cannot be opened.
        """
        if self._bus is not None:
            return

        try:
            self._bus = SMBus(self._bus_id)
        except Exception as exc:
            raise BusError(
                f"Failed to open I²C bus {self._bus_id}"
            ) from exc

    def close(self) -> None:
        """
        Close the I²C bus.

        Safe to call multiple times.
        """
        if self._bus is None:
            return

        self._bus.close()
        self._bus = None

    @property
    def is_open(self) -> bool:
        """Return True if the bus is open."""
        return self._bus is not None

    @property
    def bus_id(self) -> int:
        """Linux I²C bus number."""
        return self._bus_id

    def _require_open(self) -> SMBus:
        """
        Return the active SMBus instance.

        Raises:
            BusError:
                If the bus has not been opened.
        """
        if self._bus is None:
            raise BusError(
                "I²C bus is not open. Call 'open()' first."
            )

        return self._bus

    def read_byte(self, address: int) -> int:
        """
        Read a single byte from an I²C device.

        Args:
            address:
                7-bit device address.

        Returns:
            Integer value (0-255).

        Raises:
            DeviceCommunicationError:
                If communication fails.
        """
        bus = self._require_open()

        try:
            return bus.read_byte(address)
        except Exception as exc:
            raise DeviceCommunicationError(
                f"Failed to read byte from device 0x{address:02X}"
            ) from exc

    def write_byte(self, address: int, value: int) -> None:
        """
        Write one byte to an I²C device.

        Args:
            address:
                7-bit device address.

            value:
                Byte value (0-255).

        Raises:
            DeviceCommunicationError:
                If communication fails.
        """
        bus = self._require_open()

        try:
            bus.write_byte(address, value)
        except Exception as exc:
            raise DeviceCommunicationError(
                f"Failed to write byte to device 0x{address:02X}"
            ) from exc

    def read_register(self, address: int, register: int) -> int:
        """
        Read one register from an I²C device.

        Args:
            address:
                Device address.

            register:
                Register address.

        Returns:
            Register value.
        """
        bus = self._require_open()

        try:
            return bus.read_byte_data(address, register)
        except Exception as exc:
            raise DeviceCommunicationError(
                f"Failed to read register 0x{register:02X} "
                f"from device 0x{address:02X}"
            ) from exc

    def write_register(
        self,
        address: int,
        register: int,
        value: int,
    ) -> None:
        """
        Write one register.

        Args:
            address:
                Device address.

            register:
                Register address.

            value:
                Register value.
        """
        bus = self._require_open()

        try:
            bus.write_byte_data(address, register, value)
        except Exception as exc:
            raise DeviceCommunicationError(
                f"Failed to write register 0x{register:02X} "
                f"to device 0x{address:02X}"
            ) from exc

    def read_block(
        self,
        address: int,
        register: int,
        length: int,
    ) -> list[int]:
        """
        Read multiple bytes.

        Args:
            address:
                Device address.

            register:
                Starting register.

            length:
                Number of bytes.

        Returns:
            List of bytes.
        """
        bus = self._require_open()

        try:
            return bus.read_i2c_block_data(
                address,
                register,
                length,
            )
        except Exception as exc:
            raise DeviceCommunicationError(
                f"Failed to read block from device 0x{address:02X}"
            ) from exc

    def write_block(
        self,
        address: int,
        register: int,
        data: list[int],
    ) -> None:
        """
        Write multiple bytes.

        Args:
            address:
                Device address.

            register:
                Starting register.

            data:
                Data bytes.
        """
        bus = self._require_open()

        try:
            bus.write_i2c_block_data(
                address,
                register,
                data,
            )
        except Exception as exc:
            raise DeviceCommunicationError(
                f"Failed to write block to device 0x{address:02X}"
            ) from exc
