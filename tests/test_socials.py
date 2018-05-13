#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `socials` package."""

import pytest

from click.testing import CliRunner

import socials
from socials import cli


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'socials.cli.main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output


def test_extract():
    """Test the extract method."""
    urls = [
        'http://google.de',
        'http://facebook.com',
        'http://facebook.com/peterparker',
    ]
    matches = socials.extract(urls)
    assert 'facebook' in matches
    assert matches['facebook'][0] == urls[2]
    assert len(matches['facebook']) == 1
