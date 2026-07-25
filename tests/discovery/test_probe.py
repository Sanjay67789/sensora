from sensora.buses.i2c import I2CBus
from sensora.discovery.probe import I2CProbe

bus = I2CBus(1)
bus.open()

probe = I2CProbe(bus)

for address in range(0x03, 0x78):
    if probe.exists(address):
        print(f"Device found at 0x{address:02X}")

bus.close()
