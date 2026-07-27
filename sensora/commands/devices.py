"""
Devices command for Sensora.
"""

import typer

app = typer.Typer(
    help="List supported hardware devices.",
)


@app.callback(invoke_without_command=True)
def main() -> None:
    """
    List supported hardware devices.
    """
    typer.echo("Devices command is not implemented yet.")
