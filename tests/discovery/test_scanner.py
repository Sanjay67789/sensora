from sensora.discovery.i2c import I2CScanner
from sensora.discovery.scanner import Scanner

scanner = Scanner()
scanner.register(I2CScanner())

devices = scanner.scan()

print(f"Found {len(devices)} device(s)\n")

for device in devices:
    print(
        f"{device.name} | "
        f"Address: 0x{device.address:02X}"
    )
