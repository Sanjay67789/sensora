"""Tests for Sensora enums."""

from sensora.core.enums import BusType, DeviceStatus


def test_bus_type():
    print("BusType.I2C        :", BusType.I2C)
    print("BusType.I2C.value  :", BusType.I2C.value)
    print("BusType.SPI.value  :", BusType.SPI.value)


def test_device_status():
    print("Status             :", DeviceStatus.DETECTED)
    print("Status.value       :", DeviceStatus.DETECTED.value)


if __name__ == "__main__":
    test_bus_type()
    print()
    test_device_status()
