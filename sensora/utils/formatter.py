"""CLI output formatter for Sensora devices."""

from __future__ import annotations

import typer

from sensora.core.device import Device


class DeviceFormatter:
    """Formats Device objects for CLI output."""

    def print_summary(self, index: int, device: Device) -> None:
        typer.echo(f"[{index}] {device.name}")
        self._field("Bus", device.bus.name)
        self._field("Address", self._format_address(device.address))
        self._field("Manufacturer", device.manufacturer or "Unknown")
        self._field("Status", device.status.name)
        if device.description:
            self._field("Description", device.description)
        typer.echo()

    def print_verbose(self, index: int, device: Device) -> None:
        self._title(index, device)
        self._general(device)
        self._identification(device)
        self._interfaces(device)
        self._measurements(device)
        self._features(device)
        self._electrical(device)
        self._linux(device)
        self._metadata(device)
        self._notes(device)
        typer.echo()
        typer.echo("═" * 70)
        typer.echo()

    def print_debug(self, index: int, device: Device) -> None:
        self.print_verbose(index, device)
        self._scan(device)

    def _title(self, index: int, device: Device) -> None:
        typer.echo(f"[{index}] {device.name}")
        typer.echo("═" * 46)

    def _section(self, title: str) -> None:
        typer.echo()
        typer.echo(title)
        typer.echo("─" * 46)

    def _field(self, name: str, value: object) -> None:
        typer.echo(f"    {name:<16} : {value}")

    def _bullet(self, text: str) -> None:
        typer.echo(f"    • {text}")

    def _format_address(self, address: int | None) -> str:
        return "N/A" if address is None else hex(address)

    def _dict(self, title: str, values: dict) -> None:
        if not values:
            return
        self._section(title)
        for key, value in values.items():
            key = key.replace("_", " ").title()
            if isinstance(value, dict):
                self._field(key, "")
                for sk, sv in value.items():
                    self._field(f"  {sk.replace('_',' ').title()}", sv)
            elif isinstance(value, list):
                self._field(key, ", ".join(map(str, value)))
            else:
                self._field(key, value)

    def _list(self, title: str, values: list) -> None:
        if not values:
            return
        self._section(title)
        for value in values:
            self._bullet(str(value))

    def _general(self, device: Device) -> None:
        self._section("General")
        self._field("Name", device.name)
        self._field("Vendor", device.manufacturer or "Unknown")
        self._field("Bus", device.bus.name)
        self._field("Address", self._format_address(device.address))
        self._field("Status", device.status.name)
        if device.description:
            self._field("Description", device.description)

    def _identification(self, device: Device) -> None:
        self._dict("Identification", device.metadata.get("identification", {}))

    def _interfaces(self, device: Device) -> None:
        self._dict("Interfaces", device.metadata.get("interfaces", {}))

    def _measurements(self, device: Device) -> None:
        self._list("Measurements", device.metadata.get("measurements", []))

    def _features(self, device: Device) -> None:
        self._dict("Features", device.metadata.get("features", {}))

    def _electrical(self, device: Device) -> None:
        self._dict("Electrical", device.metadata.get("electrical", {}))

    def _linux(self, device: Device) -> None:
        linux = dict(device.metadata.get("linux", {}))
        driver = device.metadata.get("driver")
        if driver:
            linux["driver"] = driver
        self._dict("Linux", linux)

    def _metadata(self, device: Device) -> None:
        ignore = {
            "interfaces",
            "identification",
            "measurements",
            "features",
            "electrical",
            "linux",
            "driver",
            "notes",
        }
        data = {k: v for k, v in device.metadata.items() if k not in ignore}
        self._dict("Metadata", data)

    def _notes(self, device: Device) -> None:
        self._list("Notes", device.metadata.get("notes", []))

    def _scan(self, device: Device) -> None:
        self._section("Scan")
        self._field("Identified", device.metadata.get("identified", False))
        self._field("Definition ID", device.metadata.get("definition_id", "Unknown"))
        self._field("Chip ID", device.chip_id if device.chip_id is not None else "N/A")
