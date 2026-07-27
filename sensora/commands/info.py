"""
Info command for Sensora.
"""

import typer

app = typer.Typer(
    help="Display detailed information about detected hardware devices.",
)


@app.callback(invoke_without_command=True)
def main() -> None:
    """
    Display detailed information about detected hardware devices.
    """
    typer.echo("Info command is not implemented yet.")
