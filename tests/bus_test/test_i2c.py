from sensora.buses.i2c import I2CBus


def test_i2c_bus():
    bus = I2CBus()

    print(bus.is_open)

    bus.open()

    print(bus.is_open)

    bus.close()

    print(bus.is_open)


if __name__ == "__main__":
    test_i2c_bus()
