# Extraction

The `Extractor` class and `Extraction` result object are the main interfaces for parsing URLs.

## Quick Start

```python
import socials

url = socials.parse("https://github.com/lorey/socials")
print(url.platform)
# "github"

print(url.entity_type)
# "repo"

print(url.owner)
# "lorey"

urls = [
    "https://github.com/lorey",
    "https://twitter.com/karllorey",
    "https://example.com",
]
extraction = socials.parse_all(urls)
print(extraction.all())
# [GitHubProfileURL(...), TwitterProfileURL(...)]
```

## The Extractor Class

`Extractor` is the engine that parses URLs. The module-level `socials.parse()` and `socials.parse_all()` functions use a default Extractor internally.

### Creating an Extractor

```python
from socials import Extractor

# Default: all platforms
extractor = Extractor()

# Only specific platforms
extractor = Extractor(platforms=["github", "twitter"])

# Strict mode: raise error for unrecognized URLs
extractor = Extractor(strict=True)
```

### Extractor Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `parse(url)` | `SocialsURL \| None` | Parse single URL |
| `extract(urls)` | `Extraction` | Parse multiple URLs |

### Strict Mode

By default, unrecognized URLs return `None`. With `strict=True`, they raise `ParseError`:

```python
from socials import Extractor
from socials.protocols import ParseError

ext = Extractor()
print(ext.parse("https://example.com"))
# None

ext = Extractor(strict=True)
try:
    ext.parse("https://example.com")
except ParseError:
    print("Parse error raised")
# Parse error raised
```

### Platform Filtering

Limit which platforms are recognized:

```python
from socials import Extractor

ext = Extractor(platforms=["github", "twitter"])
print(ext.parse("https://linkedin.com/in/karllorey"))
# None

print(ext.parse("https://github.com/lorey"))
# GitHubProfileURL(...)
```

Available platforms: `github`, `twitter`, `linkedin`, `facebook`, `instagram`, `youtube`, `email`, `phone`

## The Extraction Class

`Extraction` is a container for parsed results with helper methods for grouping and filtering.

### Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `all()` | `list[SocialsURL]` | All parsed URL objects |
| `by_platform()` | `dict[str, list[SocialsURL]]` | Group by platform |
| `by_type()` | `dict[str, list[SocialsURL]]` | Group by entity type |

### Grouping Results

```python
import socials

urls = [
    "https://github.com/lorey",
    "https://github.com/lorey/socials",
    "https://twitter.com/karllorey",
]
extraction = socials.parse_all(urls)

print(extraction.by_platform())
# {"github": [GitHubProfileURL(...), GitHubRepoURL(...)], "twitter": [...]}

print(extraction.by_type())
# {"profile": [GitHubProfileURL(...), TwitterProfileURL(...)], "repo": [...]}
```

### Filtering

```python
import socials

urls = ["https://github.com/lorey", "https://twitter.com/karllorey"]
extraction = socials.parse_all(urls)

github_urls = extraction.by_platform().get("github", [])
print(len(github_urls))
# 1

profiles = extraction.by_type().get("profile", [])
print(len(profiles))
# 2
```

## Module-Level Functions

For convenience, socials provides module-level functions that use a default Extractor:

```python
import socials

socials.parse("https://github.com/lorey")
# Parse single URL

socials.parse_all(["https://github.com/lorey"])
# Parse multiple URLs
```

## Legacy API (0.x Compatibility)

For backwards compatibility with 0.x, the following are deprecated:

**Deprecated module function:**
```python
import socials

# Deprecated - use parse_all() instead
socials.extract(["https://github.com/lorey"])
```

**Deprecated Extraction methods** (return URL strings instead of typed objects):
```python
import socials

extraction = socials.parse_all(["https://github.com/lorey"])

# Deprecated (returns strings)
extraction.get_matches_per_platform()
extraction.get_matches_for_platform("github")

# Use instead (returns typed objects)
extraction.by_platform()
extraction.by_platform()["github"]
```

These methods emit deprecation warnings and will be removed in a future version.
