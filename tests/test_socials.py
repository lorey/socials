"""Tests for `socials` CLI."""

from typer.testing import CliRunner

from socials.cli import app

runner = CliRunner()


def test_cli_help():
    """Test CLI help output."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Extract social media profile URLs" in result.output


def test_cli_version():
    """Test CLI version output."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "socials" in result.output


def test_cli_check():
    """Test CLI check command."""
    result = runner.invoke(app, ["check", "https://github.com/lorey"])
    assert result.exit_code == 0
    assert "github" in result.output

    result = runner.invoke(app, ["check", "https://example.com"])
    assert result.exit_code == 1


def test_cli_extract():
    """Test CLI extract command."""
    result = runner.invoke(
        app,
        ["extract"],
        input="https://github.com/lorey\nhttps://twitter.com/karllorey\n",
    )
    assert result.exit_code == 0
    assert "github" in result.output
    assert "twitter" in result.output
