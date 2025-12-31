"""Tests for `socials` package."""

import warnings

from typer.testing import CliRunner

import socials
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


def test_extract():
    """Test the extract method with deprecated 0.x API."""
    # Suppress deprecation warnings for this test since we're testing legacy API
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    urls = [
        "http://google.de",
        "http://facebook.com",
        "http://facebook.com/peterparker",
        "http://facebook.com/peter[parker",  # Invalid character
        "https://www.facebook.com/profile.php?id=4",
        "mailto:bill@microsoft.com",
        "steve@microsoft.com",
        "https://www.linkedin.com/company/google/",
        "https://www.linkedin.com/comp^any/google/",  # Invalid character
        "http://www.twitter.com/Some_Company/",
        "http://www.twitter.com/Some_\\Company",  # Invalid character
        "https://www.instagram.com/instagram/",
        "https://www.instagram.com/instag-ram/",  # Invalid character
        "http://instagr.am/instagram",
        "http://youtube.com/this/is/too/long",
        "http://www.youtube.com/user/Some_1",
        "http://youtube.com/c/your-custom-name",
        "http://youtube.com/your.custom.name",
    ]
    extraction = socials.extract(urls)
    matches = extraction.get_matches_per_platform()
    assert "facebook" in matches
    assert len(matches["facebook"]) == 2
    assert "http://facebook.com/peterparker" in matches["facebook"]
    assert "https://www.facebook.com/profile.php?id=4" in matches["facebook"]

    assert "email" in matches
    assert len(matches["email"]) == 2
    assert "bill@microsoft.com" in matches["email"]
    assert "steve@microsoft.com" in matches["email"]

    assert "linkedin" in matches
    assert len(matches["linkedin"]) == 1
    assert "https://www.linkedin.com/company/google/" in matches["linkedin"]

    assert "twitter" in matches
    assert len(matches["twitter"]) == 1
    assert "http://www.twitter.com/Some_Company/" in matches["twitter"]

    assert "instagram" in matches
    assert len(matches["instagram"]) == 2
    assert "https://www.instagram.com/instagram/" in matches["instagram"]
    assert "http://instagr.am/instagram" in matches["instagram"]

    assert "youtube" in matches
    assert len(matches["youtube"]) == 3
    assert "http://www.youtube.com/user/Some_1" in matches["youtube"]
    assert "http://youtube.com/c/your-custom-name" in matches["youtube"]
    assert "http://youtube.com/your.custom.name" in matches["youtube"]
