from sensora.discovery.i2c import I2CScanner

scanner = I2CScanner()

result = scanner.scan()

print(result.message)

for device in result.devices:
    print(
        f"{device.name} | "
        f"Address: 0x{device.address:02X}"
    )
