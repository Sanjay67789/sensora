"""Scan command for Sensora."""

from __future__ import annotations

import json

import typer

from sensora.buses.linux.onewire import LinuxOneWireBus
from sensora.database.loader import DatabaseLoader
from sensora.database.matcher import DeviceMatcher
from sensora.discovery.i2c import I2CScanner
from sensora.discovery.onewire import OneWireScanner
from sensora.discovery.scanner import Scanner
from sensora.discovery.spi import SPIScanner
from sensora.discovery.uart import UARTScanner
from sensora.utils.formatter import DeviceFormatter

app = typer.Typer(help="Scan the system for supported hardware devices.")


@app.callback(invoke_without_command=True)
def main(
    bus: str = typer.Option(
        "all", "--bus", "-b", help="Bus to scan (all, i2c, spi, uart, onewire)."
    ),
    json_output: bool = typer.Option(
        False, "--json", help="Output scan results as JSON."
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose output."
    ),
    debug: bool = typer.Option(False, "--debug", help="Enable debug output."),
) -> None:
    registry = DatabaseLoader().load()
    matcher = DeviceMatcher(registry)
    scanner = Scanner()

    match bus.lower():
        case "all":
            scanner.register(I2CScanner(matcher=matcher))
            scanner.register(SPIScanner())
            scanner.register(UARTScanner())
            scanner.register(OneWireScanner(LinuxOneWireBus()))
        case "i2c":
            scanner.register(I2CScanner(matcher=matcher))
        case "spi":
            scanner.register(SPIScanner())
        case "uart":
            scanner.register(UARTScanner())
        case "onewire":
            scanner.register(OneWireScanner(LinuxOneWireBus()))
        case _:
            typer.secho(f"Unsupported bus '{bus}'.", fg=typer.colors.RED)
            raise typer.Exit(code=1)

    if verbose or debug:
        typer.secho("Scanning hardware...", fg=typer.colors.CYAN)

    result = scanner.scan()
    devices = result.devices
    formatter = DeviceFormatter()

    if json_output:
        typer.echo(
            json.dumps(
                [
                    {
                        "name": d.name,
                        "bus": d.bus.name,
                        "manufacturer": d.manufacturer,
                        "address": hex(d.address) if d.address is not None else None,
                        "status": d.status.name,
                        "description": d.description,
                        "metadata": d.metadata,
                    }
                    for d in devices
                ],
                indent=4,
            )
        )
        return

    typer.echo()

    if not devices:
        typer.secho("No supported devices found.", fg=typer.colors.YELLOW)
        if verbose or debug:
            for bus_result in result.buses:
                typer.echo(f"{bus_result.name}: {bus_result.message}")
        typer.echo(f"Scan completed in {result.duration:.3f} s")
        return

    typer.secho(f"Found {len(devices)} device(s)\n", fg=typer.colors.GREEN, bold=True)

    for index, device in enumerate(devices, start=1):
        if debug:
            formatter.print_debug(index=index, device=device)
        elif verbose:
            formatter.print_verbose(index=index, device=device)
        else:
            formatter.print_summary(index=index, device=device)

        if index != len(devices):
            typer.echo()
            typer.echo()

    typer.secho(
        f"Scan completed in {result.duration:.3f} s",
        fg=typer.colors.BLUE,
    )
