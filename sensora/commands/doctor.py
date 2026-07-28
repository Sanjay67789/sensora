"""
Doctor command for Sensora.
"""

from __future__ import annotations

import typer

from sensora.diagnostics.health import HealthDiagnostics

app = typer.Typer(
    help="Check Sensora system health.",
)


@app.callback(invoke_without_command=True)
def main() -> None:
    """
    Run Sensora health diagnostics.
    """

    typer.echo()

    typer.secho(
        "Sensora Doctor",
        fg=typer.colors.CYAN,
        bold=True,
    )

    typer.echo()

    diagnostics = HealthDiagnostics()

    results = diagnostics.run()

    warning_count = 0
    failure_count = 0

    for result in results:

        if result.status == "PASS":
            symbol = "✓"
            color = typer.colors.GREEN

        elif result.status == "WARN":
            symbol = "⚠"
            color = typer.colors.YELLOW
            warning_count += 1

        else:
            symbol = "✗"
            color = typer.colors.RED
            failure_count += 1

        typer.secho(
            f"{symbol} {result.name}",
            fg=color,
            bold=True,
        )

        typer.echo(
            f"    {result.message}"
        )

        if result.causes:
            typer.echo()

            typer.echo(
                "    Possible causes:"
            )

            for cause in result.causes:
                typer.echo(
                    f"      - {cause}"
                )

        if result.suggestions:
            typer.echo()

            typer.echo(
                "    Recommended:"
            )

            for suggestion in result.suggestions:
                typer.echo(
                    f"      - {suggestion}"
                )

        typer.echo()

    typer.secho(
        "Health Summary",
        fg=typer.colors.CYAN,
        bold=True,
    )

    typer.echo()

    if failure_count:
        typer.secho(
            "FAILED",
            fg=typer.colors.RED,
            bold=True,
        )

    elif warning_count:
        typer.secho(
            "GOOD WITH WARNINGS",
            fg=typer.colors.YELLOW,
            bold=True,
        )

    else:
        typer.secho(
            "EXCELLENT",
            fg=typer.colors.GREEN,
            bold=True,
        )
