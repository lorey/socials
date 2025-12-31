"""Console script for socials."""

from __future__ import annotations

import sys
from typing import Optional

import typer

import socials
from socials.platforms import DEFAULT_PARSERS

app = typer.Typer(
    help="Extract social media profile URLs from a list of URLs.",
    no_args_is_help=True,
)

# Get available platform names from default parsers
AVAILABLE_PLATFORMS = list(DEFAULT_PARSERS.keys())


def version_callback(value: bool) -> None:
    """Print version and exit if --version flag is set."""
    if value:
        typer.echo(f"socials {socials.__version__}")
        raise typer.Exit


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit.",
    ),
) -> None:
    """Social Account Detection for Python."""


@app.command()
def extract(
    file: Optional[typer.FileText] = typer.Argument(
        None,
        help="File containing URLs (one per line). Reads from stdin if not provided.",
    ),
    platform: Optional[str] = typer.Option(
        None,
        "--platform",
        "-p",
        help=f"Filter by platform: {', '.join(AVAILABLE_PLATFORMS)}",
    ),
) -> None:
    """Extract social media URLs from input."""
    if file is None:
        if sys.stdin.isatty():
            typer.echo(
                "Error: No input provided. Pipe URLs or specify a file.",
                err=True,
            )
            raise typer.Exit(1)
        lines = sys.stdin.read().strip().split("\n")
    else:
        lines = file.read().strip().split("\n")

    urls = [line.strip() for line in lines if line.strip()]
    extraction = socials.extract(urls)

    if platform:
        if platform not in AVAILABLE_PLATFORMS:
            typer.echo(f"Error: Unknown platform '{platform}'", err=True)
            typer.echo(f"Available: {', '.join(AVAILABLE_PLATFORMS)}", err=True)
            raise typer.Exit(1)
        by_plat = extraction.by_platform()
        for url_obj in by_plat.get(platform, []):
            typer.echo(url_obj.url)
    else:
        for url_obj in extraction.all():
            typer.echo(f"{url_obj.platform}\t{url_obj.url}")


@app.command()
def check(
    url: str = typer.Argument(..., help="URL to check"),
) -> None:
    """Check which platform a URL belongs to."""
    result = socials.parse(url)
    if result:
        typer.echo(result.platform)
    else:
        typer.echo("unknown", err=True)
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
