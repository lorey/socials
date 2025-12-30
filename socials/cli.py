"""Console script for socials."""

import sys
from typing import Optional

import typer

import socials
from socials.socials import PATTERNS, get_platform

app = typer.Typer(
    help="Extract social media profile URLs from a list of URLs.",
    no_args_is_help=True,
)


def version_callback(value: bool) -> None:
    if value:
        typer.echo(f"socials {socials.__version__}")
        raise typer.Exit()


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
    pass


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
        help=f"Filter by platform: {', '.join(PATTERNS.keys())}",
    ),
) -> None:
    """Extract social media URLs from input."""
    if file is None:
        if sys.stdin.isatty():
            typer.echo("Error: No input provided. Pipe URLs or specify a file.", err=True)
            raise typer.Exit(1)
        lines = sys.stdin.read().strip().split("\n")
    else:
        lines = file.read().strip().split("\n")

    urls = [line.strip() for line in lines if line.strip()]
    extraction = socials.extract(urls)

    if platform:
        if platform not in PATTERNS:
            typer.echo(f"Error: Unknown platform '{platform}'", err=True)
            typer.echo(f"Available: {', '.join(PATTERNS.keys())}", err=True)
            raise typer.Exit(1)
        matches = extraction.get_matches_for_platform(platform)
        for url in matches:
            typer.echo(url)
    else:
        results = extraction.get_matches_per_platform()
        for plat, matches in results.items():
            for url in matches:
                typer.echo(f"{plat}\t{url}")


@app.command()
def check(
    url: str = typer.Argument(..., help="URL to check"),
) -> None:
    """Check which platform a URL belongs to."""
    platform = get_platform(url)
    if platform:
        typer.echo(platform)
    else:
        typer.echo("unknown", err=True)
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
