# Socials

[![PyPI](https://img.shields.io/pypi/v/socials.svg)](https://pypi.python.org/pypi/socials)
[![CI](https://github.com/lorey/socials/actions/workflows/ci.yml/badge.svg)](https://github.com/lorey/socials/actions/workflows/ci.yml)
[![Documentation](https://readthedocs.org/projects/socials/badge/?version=latest)](https://socials.readthedocs.io/en/latest/?badge=latest)

Social Account Detection and Extraction for Python

- Free software: GNU General Public License v3
- Documentation: https://socials.readthedocs.io
- Source: https://github.com/lorey/socials

## Features

- Detect and extract URLs of social accounts: throw in URLs, get back URLs of social media profiles by type.
- Supports Facebook, Twitter, LinkedIn, GitHub, Instagram, YouTube, and email addresses.

## Installation

```bash
pip install socials
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv add socials
```

## Usage

### Python API

```python
import socials

hrefs = [
    "https://facebook.com/peterparker",
    "https://techcrunch.com",
    "https://github.com/lorey",
]

# Get all matches grouped by platform
socials.extract(hrefs).get_matches_per_platform()
# {'facebook': ['https://facebook.com/peterparker'], 'github': ['https://github.com/lorey'], ...}

# Get matches for a specific platform
socials.extract(hrefs).get_matches_for_platform("github")
# ['https://github.com/lorey']
```

### CLI

```bash
# Check which platform a URL belongs to
socials check https://github.com/lorey
# github

# Extract social URLs from a file
socials extract urls.txt

# Extract from stdin
echo "https://github.com/lorey" | socials extract
```

## Socials API

There's also [Socials API](https://github.com/lorey/socials-api) that allows you to use the functionality via REST.
You can use a [free online version](https://socials.karllorey.com), try it in the browser, or deploy it yourself.

## Development

```bash
# Clone and install
git clone https://github.com/lorey/socials
cd socials
uv sync --extra dev

# Run tests
uv run pytest

# Run linting
uv run ruff check .
uv run mypy socials

# Format code
uv run ruff format .
```
