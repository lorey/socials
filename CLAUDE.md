# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Socials is a Python library for detecting and extracting social media profile URLs from a list of hrefs. It uses regex pattern matching to identify URLs from Facebook, Twitter, LinkedIn, GitHub, Instagram, YouTube, and email addresses.

## Development Commands

```bash
# Setup
virtualenv -p /usr/bin/python3 venv
source venv/bin/activate
pip install -r requirements-dev.txt

# Testing
tox                      # Multi-Python version testing
python setup.py test     # Single test run
make test                # Alternative: runs py.test

# Linting
make lint                # Runs flake8 socials tests

# Coverage
make coverage            # Generates HTML coverage report

# Release (requires bumpversion)
bumpversion patch && git push --tags
```

## Architecture

The library is a single-module design in `socials/socials.py`:

- **Platform constants**: `PLATFORM_FACEBOOK`, `PLATFORM_GITHUB`, etc.
- **Regex patterns**: Each platform has a list of regex patterns (e.g., `FACEBOOK_URL_REGEXS`)
- **PATTERNS dict**: Maps platform constants to their regex lists
- **Extraction class**: Wrapper returned by `socials.extract()` with methods:
  - `get_matches_per_platform()` - returns dict of all matches by platform
  - `get_matches_for_platform(platform)` - returns list for specific platform
- **Cleaners**: Optional post-processing functions (e.g., `clean_mailto` strips `mailto:` prefix)

## Adding a New Platform

1. Add platform constant: `PLATFORM_X = 'x'`
2. Add regex list: `X_URL_REGEXS = [r'^http(s)?://...']`
3. Add to `PATTERNS` dict
4. Add test cases in `tests/test_socials.py`
5. If needed, add cleaner function and register in `get_cleaner()`

## Regex Conventions

- All patterns use `^` and `$` anchors for exact matching
- Character classes use `[A-Za-z0-9_-]` (avoiding chars between Z and a in ASCII)
- Optional trailing slash: `/?$`
- Optional https: `http(s)?://`
- Optional www: `(www\.)?`
