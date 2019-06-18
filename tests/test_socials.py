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
        'http://facebook.com/peter[parker',  # Invalid character
        'mailto:bill@microsoft.com',
        'steve@microsoft.com',
        'https://www.linkedin.com/company/google/',
        'https://www.linkedin.com/comp^any/google/',  # Invalid character
        'http://www.twitter.com/Some_Company/',
        'http://www.twitter.com/Some_\\Company',  # Invalid character
        'https://www.instagram.com/instagram/',
        'https://www.instagram.com/instag-ram/',  # Invalid character
        'http://instagr.am/instagram',
    ]
    extraction = socials.extract(urls)
    matches = extraction.get_matches_per_platform()
    assert 'facebook' in matches
    assert matches['facebook'][0] == urls[2]
    assert len(matches['facebook']) == 1

    assert 'email' in matches
    assert len(matches['email']) == 2
    assert 'bill@microsoft.com' in matches['email']
    assert 'steve@microsoft.com' in matches['email']

    assert 'linkedin' in matches
    assert len(matches['linkedin']) == 1
    assert matches['linkedin'][0] == 'https://www.linkedin.com/company/google/'

    assert 'twitter' in matches
    assert len(matches['twitter']) == 1
    assert matches['twitter'][0] == 'http://www.twitter.com/Some_Company/'

    assert 'instagram' in matches
    assert len(matches['instagram']) == 2
    assert matches['instagram'][0] == 'https://www.instagram.com/instagram/'
    assert matches['instagram'][1] == 'http://instagr.am/instagram'
