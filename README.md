# Socials

[![PyPI](https://img.shields.io/pypi/v/socials.svg)](https://pypi.python.org/pypi/socials)
[![CI](https://github.com/lorey/socials/actions/workflows/ci.yml/badge.svg)](https://github.com/lorey/socials/actions/workflows/ci.yml)
[![Documentation](https://readthedocs.org/projects/socials/badge/?version=latest)](https://socials.readthedocs.io/en/latest/?badge=latest)

Social Account Detection and Extraction for Python

- Free software: GNU General Public License v3
- Documentation: https://socials.readthedocs.io
- Source: https://github.com/lorey/socials

## Features

- Parse social URLs into typed objects with extracted fields (username, repo, etc.)
- Supports Facebook, Twitter/X, LinkedIn, GitHub, Instagram, YouTube, email, and phone
- Navigate URL hierarchies (e.g., repo -> profile)
- Filter and group results by platform or entity type

## Installation

```bash
pip install socials
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv add socials
```

## Usage

### Parse a single URL

```python
import socials

result = socials.parse("https://github.com/lorey/socials")
result.platform      # "github"
result.entity_type   # "repo"
result.owner         # "lorey"
result.repo          # "socials"
```

### Navigate hierarchies

```python
result = socials.parse("https://github.com/lorey/socials")
parent = result.get_parent()  # GitHubProfileURL for the owner
parent.username  # "lorey"
```

### Extract from multiple URLs

```python
urls = [
    "https://github.com/lorey",
    "https://twitter.com/karllorey",
    "mailto:test@example.com",
    "https://example.com",  # ignored
]

extraction = socials.extract(urls)
extraction.all()          # list of all parsed URLs
extraction.by_platform()  # {'github': [...], 'twitter': [...], 'email': [...]}
extraction.by_type()      # {'profile': [...], 'email': [...]}
```

### Custom extractor with platform filtering

```python
# Only extract GitHub and Twitter URLs
ext = socials.Extractor(platforms=["github", "twitter"])
ext.parse("https://github.com/lorey")  # works
ext.parse("mailto:test@example.com")   # returns None

# Strict mode - raise error for unknown URLs
ext = socials.Extractor(strict=True)
ext.parse("https://unknown.com")  # raises ParseError
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

## Supported Platforms

| Platform | Entity Types |
|----------|--------------|
| GitHub | profile, repo |
| Twitter/X | profile |
| LinkedIn | profile, company |
| Facebook | profile |
| Instagram | profile |
| YouTube | channel |
| Email | email |
| Phone | phone |

## Migrating from 0.x

The 0.x API still works but is deprecated:

```python
# Old API (deprecated)
extraction.get_matches_per_platform()  # returns dict[str, list[str]]
extraction.get_matches_for_platform("github")

# New API (1.0+)
extraction.by_platform()  # returns dict[str, list[SocialsURL]]
extraction.all()          # returns list[SocialsURL]
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
