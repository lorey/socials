# socials

[![PyPI](https://img.shields.io/pypi/v/socials.svg)](https://pypi.python.org/pypi/socials)
[![CI](https://github.com/lorey/socials/actions/workflows/ci.yml/badge.svg)](https://github.com/lorey/socials/actions/workflows/ci.yml)
[![Documentation](https://readthedocs.org/projects/socials/badge/?version=latest)](https://socials.readthedocs.io/en/latest/?badge=latest)

[Documentation](https://socials.readthedocs.io) | [Source Code](https://github.com/lorey/socials)

Python library and CLI to turn URLs into structured social media profiles.

You have a list of URLs from a scrape, a CSV export, or email signatures.
Some of them are social media profiles.
Socials finds them and gives you structured data to work with.

| | |
|---|---|
| :mag: **Extract** | Pull social profiles from scraped pages or contact lists |
| :white_check_mark: **Validate** | Check if URLs are recognized social profiles |
| :arrows_counterclockwise: **Normalize** | Get consistent usernames from messy URL variations |
| :card_file_box: **Categorize** | Group URLs by platform or entity type |
| :robot: **Automate** | Batch process URL files via CLI |

## Installation

**Note:** This README documents the upcoming 1.0 release.
To try it, install with pre-release support:

```bash
pip install --pre socials
# or
uv add --pre socials
```

Feedback welcome at [GitHub Issues](https://github.com/lorey/socials/issues).

For the current stable version (0.3.x), use `pip install socials` and see the
[v0.3.0 documentation](https://github.com/lorey/socials/tree/v0.3.0).

## Quick Example

```python
import socials

# Parse a single URL
repo = socials.parse("https://github.com/lorey/socials")
print(repo)
# GitHubRepoURL(owner='lorey', repo='socials')

print(repo.platform)
# 'github'

print(repo.owner)
# 'lorey'

# Parse multiple URLs at once
urls = ["https://github.com/lorey", "https://twitter.com/karllorey", "https://example.com"]
result = socials.parse_all(urls)

print(result.all())
# [GitHubProfileURL(username='lorey'), TwitterProfileURL(username='karllorey')]

print(result.by_platform())
# {'github': [...], 'twitter': [...]}
```

## Why socials?

- **Structured data, not strings.** You get typed Python objects with extracted fields like `username`, `repo`, or `company`. Not just a matched URL string.
- **Handles the edge cases.** With or without `www`. Trailing slashes or not. Old URL formats. Mobile URLs. Socials normalizes them all.
- **Comprehensive platform coverage.** 8 platforms with multiple entity types each. Profiles, repos, companies, channels. Continuously updated as platforms change their URL formats.
- **Extensible.** Need to support an internal tool or a platform we don't cover? Register your own parser and it works with the same API.
- **Built for messy real-world data.** Lenient by default. Unknown URLs return `None` instead of crashing. Strict mode available when you need validation.
- **Type-safe with IDE support.** Full type hints. Autocomplete works. Catch bugs before runtime.

## Features

### Typed URL Objects

Each parsed URL is a typed object with platform-specific fields:

```python
import socials

company = socials.parse("https://linkedin.com/company/acme-corp")
print(company)
# LinkedInCompanyURL(company_name='acme-corp')

print(company.platform)
# 'linkedin'

print(company.entity_type)
# 'company'
```

### Hierarchy Navigation

Navigate from a repo to its owner, or from any URL to its root:

```python
import socials

repo = socials.parse("https://github.com/lorey/socials")
print(repo.get_parent())
# GitHubProfileURL(username='lorey')
```

### Batch Extraction

Parse many URLs at once and group the results:

```python
import socials

urls = ["https://github.com/lorey", "https://twitter.com/karllorey"]
result = socials.parse_all(urls)

result.all()
# list of all parsed URLs

result.by_platform()
# {'github': [...], 'twitter': [...]}

result.by_type()
# {'profile': [...]}
```

### Platform Filtering

Only extract what you need:

```python
import socials

extractor = socials.Extractor(platforms=["github", "linkedin"])
print(extractor.parse("https://twitter.com/someone"))
# None
```

## Supported Platforms

| Platform   | Entity Types     | Example Fields          |
|------------|------------------|-------------------------|
| GitHub     | profile, repo    | username, owner, repo   |
| Twitter/X  | profile          | username                |
| LinkedIn   | profile, company | username, company_name  |
| Facebook   | profile          | username                |
| Instagram  | profile          | username                |
| YouTube    | channel          | channel_id, username    |
| Email      | email            | email                   |
| Phone      | phone            | phone                   |

Missing a platform? [Open an issue](https://github.com/lorey/socials/issues) or submit a PR!

## CLI

The CLI lets you process URLs directly from the command line. Run it with `uvx` (no install needed) or install globally with `pip install socials`.

```
$ uvx socials --help

Usage: socials [OPTIONS] COMMAND [ARGS]...

 Extract social media profile URLs from a list of URLs.

╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ extract   Extract social media URLs from input.                              │
│ check     Check which platform a URL belongs to.                             │
╰──────────────────────────────────────────────────────────────────────────────╯
```

Examples:

```bash
# Find all social links on a webpage
$ curl -s https://karllorey.com | grep -oE 'https?://[^"]+' | socials extract
linkedin	https://www.linkedin.com/in/karllorey
github	https://github.com/lorey
instagram	https://www.instagram.com/karllorey

# Check what platform a URL belongs to
$ socials check https://github.com/lorey
github
```

## Documentation

Full docs at [socials.readthedocs.io](https://socials.readthedocs.io)

- [Getting Started](https://socials.readthedocs.io/getting-started/) - Tutorial with examples
- [CLI Reference](https://socials.readthedocs.io/cli/) - Command-line usage
- [API Reference](https://socials.readthedocs.io/reference/) - Full API docs
- [Architecture](https://socials.readthedocs.io/architecture/) - How it works

## Related

- [Socials API](https://github.com/lorey/socials-api) - REST API wrapper. [Free hosted version](https://socials.karllorey.com) available.
- [social-media-profiles-regexs](https://github.com/lorey/social-media-profiles-regexs) - Regular expressions for social media URLs.
- [flutter_url_recognizer](https://github.com/dpajak99/flutter_url_recognizer) - Similar implementation for Flutter.

## License

GNU General Public License v3
