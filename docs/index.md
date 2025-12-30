# Socials

Social Account Detection and Extraction for Python.

## Installation

```bash
pip install socials
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv add socials
```

## Quick Start

```python
import socials

hrefs = [
    "https://facebook.com/peterparker",
    "https://techcrunch.com",
    "https://github.com/lorey",
]

# Get all matches grouped by platform
results = socials.extract(hrefs).get_matches_per_platform()
# {'facebook': ['https://facebook.com/peterparker'], 'github': ['https://github.com/lorey'], ...}

# Get matches for a specific platform
github_urls = socials.extract(hrefs).get_matches_for_platform("github")
# ['https://github.com/lorey']
```

## Supported Platforms

- Facebook
- Twitter
- LinkedIn
- GitHub
- Instagram
- YouTube
- Email addresses

## Links

- [Source Code](https://github.com/lorey/socials)
- [PyPI](https://pypi.org/project/socials/)
- [Socials API](https://github.com/lorey/socials-api) - REST API wrapper
