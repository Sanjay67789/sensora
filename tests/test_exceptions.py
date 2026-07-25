"""Tests for Sensora exceptions."""

from sensora.core.exceptions import DeviceNotFoundError


def test_exception():
    try:
        raise DeviceNotFoundError("BME280 not found")
    except DeviceNotFoundError as exc:
        print(type(exc).__name__)
        print(exc)


if __name__ == "__main__":
    test_exception()
