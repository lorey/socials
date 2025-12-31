# Architecture

This document describes the architecture of socials 1.0, designed for stability and extensibility over the next 5+ years.

## Use Cases

Social URLs are more than just profiles. They can be posts, repos, issues, videos, playlists, and more. This library addresses the following use cases:

1. **Entity detection** - What kind of thing is this URL? (profile, repo, issue, tweet, video)
2. **Identifier extraction** - Get the username, repo slug, issue number, video ID, etc.
3. **Parent relationships** - Navigate hierarchy (issue → repo → profile)
4. **Filtering by platform or type** - "Give me only GitHub profiles from this list"
5. **Batch extraction** - Process a list of scraped URLs, group by platform

Secondary (future):
- **URL building** - Construct URLs from structured data

## Package Structure

```
socials/
├── __init__.py          # Public API facade
├── protocols.py         # SocialsURL and PlatformParser protocols
├── registry.py          # Domain → parser registry
├── extractor.py         # Extractor class and Extraction result object
├── platforms/
│   ├── __init__.py      # DEFAULT_PARSERS list
│   ├── base.py          # URL utilities (extract_hostname, path parsing)
│   ├── github.py        # GitHubParser + GitHubRepoURL, GitHubProfileURL, ...
│   ├── twitter.py
│   ├── linkedin.py
│   ├── youtube.py
│   ├── facebook.py
│   ├── instagram.py
│   └── misc.py          # mailto:, tel:, etc.
└── cli/
    └── __init__.py
```

## Component Interaction

```
┌─────────────────────────────────────────────────────────┐
│              Extractor (or module-level API)            │
│                                                         │
│  socials.parse(url)                                     │
│  socials.extract(urls) → Extraction                     │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│                      Registry                           │
│                                                         │
│  extract_hostname(url) → lookup parser            │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│                   Platform Parser                       │
│                                                         │
│  GitHubParser.parse(url) → GitHubRepoURL                │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│        Typed URL (implements SocialsURL Protocol)       │
│                                                         │
│  GitHubRepoURL {url, platform, entity_type, owner, ...} │
│                                                         │
│  .get_parent() → GitHubProfileURL | None                │
│  .get_root() → GitHubProfileURL                         │
│  .get_ancestors() → list[SocialsURL]                    │
└─────────────────────────────────────────────────────────┘
```

**Flow:**

1. User calls `socials.parse(url)`
2. Registry extracts domain from URL and looks up the responsible parser
3. Parser matches URL against its patterns and returns a typed URL object
4. Typed URL implements the `SocialsURL` protocol with hierarchy traversal

## Core Data Models

### Design Principle

Platform-specific typed classes are primary, not wrappers around a generic base.
Each platform defines its own URL classes with typed fields.

### Protocols

```python
from typing import Protocol

class SocialsURL(Protocol):
    """Common interface all parsed URLs implement."""
    url: str
    platform: str
    entity_type: str

    def get_parent(self) -> "SocialsURL | None":
        """Immediate parent (issue → repo)."""
        ...

    def get_root(self) -> "SocialsURL":
        """Top of hierarchy (issue → profile/org)."""
        ...

    def get_ancestors(self) -> "list[SocialsURL]":
        """Full chain from parent to root: [repo, profile]."""
        ...


class PlatformParser(Protocol):
    """Interface for platform-specific URL parsers."""
    platform: str

    def handles_hostname(self, hostname: str) -> bool:
        """Check if this parser handles the given hostname."""
        ...

    def parse(self, url: str) -> SocialsURL | None:
        """Parse URL into typed object, or None if not recognized."""
        ...


class ParseError(Exception):
    """Raised when URL parsing fails (if strict mode enabled)."""
    pass
```

### Typed URL Classes (Example: GitHub)

```python
from typing import Literal
from pydantic import BaseModel

class GitHubProfileURL(BaseModel, frozen=True):
    url: str
    platform: Literal["github"] = "github"
    entity_type: Literal["profile"] = "profile"
    username: str

    def __hash__(self) -> int:
        return hash(self.url)

    def get_parent(self) -> None:
        return None

    def get_root(self) -> "GitHubProfileURL":
        return self

    def get_ancestors(self) -> "list[SocialsURL]":
        return []


class GitHubRepoURL(BaseModel, frozen=True):
    url: str
    platform: Literal["github"] = "github"
    entity_type: Literal["repo"] = "repo"
    owner: str
    slug: str

    def __hash__(self) -> int:
        return hash(self.url)

    def get_parent(self) -> GitHubProfileURL:
        return GitHubProfileURL(
            url=f"https://github.com/{self.owner}",
            username=self.owner,
        )

    def get_root(self) -> GitHubProfileURL:
        return self.get_parent()

    def get_ancestors(self) -> "list[SocialsURL]":
        return [self.get_parent()]


class GitHubIssueURL(BaseModel, frozen=True):
    url: str
    platform: Literal["github"] = "github"
    entity_type: Literal["issue"] = "issue"
    owner: str
    repo: str
    number: int

    def __hash__(self) -> int:
        return hash(self.url)

    def get_parent(self) -> GitHubRepoURL:
        return GitHubRepoURL(
            url=f"https://github.com/{self.owner}/{self.repo}",
            owner=self.owner,
            slug=self.repo,
        )

    def get_root(self) -> GitHubProfileURL:
        return self.get_parent().get_root()

    def get_ancestors(self) -> "list[SocialsURL]":
        parent = self.get_parent()
        return [parent] + parent.get_ancestors()
```

### Parser Example

```python
class GitHubParser:
    platform = "github"

    def handles_hostname(self, hostname: str) -> bool:
        return hostname in ["github.com", "gist.github.com", "raw.githubusercontent.com"]

    def parse(self, url: str) -> SocialsURL | None:
        # Match against patterns, return appropriate typed class
        ...


class MastodonParser:
    platform = "mastodon"

    def handles_hostname(self, hostname: str) -> bool:
        # Can check known instances, call API, or use heuristics
        return hostname in KNOWN_INSTANCES or self._verify_instance(hostname)

    def parse(self, url: str) -> SocialsURL | None:
        ...
```

## URL Evolution Handling

URLs change over time. Our strategy:

- **Domain changes** (twitter.com → x.com): Parser's `handles_hostname()` handles multiple hostnames
- **Path changes**: Parser handles multiple regex patterns, returns same typed class
- **Principle**: Lenient parsing, single output. Typed class represents the entity, not the URL format.

```python
class TwitterParser:
    platform = "twitter"

    def handles_hostname(self, hostname: str) -> bool:
        return hostname in ["twitter.com", "x.com", "t.co"]
```

## Public API

### Convenience Functions (default Extractor)

```python
import socials

# Parse single URL
result = socials.parse("https://github.com/lorey/socials")
result.platform      # "github"
result.entity_type   # "repo"
result.owner         # "lorey"
result.slug          # "socials"

# Hierarchy traversal
result.get_parent()    # GitHubProfileURL
result.get_root()      # GitHubProfileURL
result.get_ancestors() # [GitHubProfileURL]

# Parse multiple URLs → Extraction result object
extraction = socials.extract(urls)
extraction.all()                    # list[SocialsURL]
extraction.by_platform()            # dict[str, list[SocialsURL]]
extraction.by_type()                # dict[str, list[SocialsURL]]

# 0.x backwards compatibility
extraction.get_matches_per_platform()
extraction.get_matches_for_platform("github")

# Register custom parser with default Extractor
socials.register(MastodonParser())
```

### Custom Extractor

```python
import socials

# Only specific platforms
ext = socials.Extractor(platforms=["linkedin", "twitter"])
ext.extract(urls)

# Exclude some platforms
ext = socials.Extractor(exclude=["email", "phone"])

# Empty + custom parsers (for testing or special use)
ext = socials.Extractor(platforms=[])
ext.register(MastodonParser(instances=["mastodon.social"]))

# Parsers with their own state
mastodon = MastodonParser(
    instances=["mastodon.social", "fosstodon.org"],
    fetch_instances=True,  # Optionally fetch from API
)
ext = socials.Extractor()
ext.register(mastodon)
```

**Verbs:**

- `parse(url)` - single URL → typed object (or None, raises ParseError if strict=True)
- `extract(urls)` - batch → Extraction result object

**Strict mode:**

```python
# Default: return None for unrecognized URLs
result = socials.parse("https://unknown.com/page")  # None

# Strict mode: raise ParseError
ext = socials.Extractor(strict=True)
ext.parse("https://unknown.com/page")  # raises ParseError
```

## Serialization

All typed classes share common fields (`url`, `platform`, `entity_type`), so JSON output is consistent:

```python
result = socials.parse("https://github.com/lorey/socials")
result.model_dump()
# {
#     "url": "https://github.com/lorey/socials",
#     "platform": "github",
#     "entity_type": "repo",
#     "owner": "lorey",
#     "slug": "socials"
# }
```

Deserialization uses registry lookup by `(platform, entity_type)` to find the correct class.

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Typed classes vs generic dict | Typed classes (`GitHubRepoURL`) | Type safety, IDE support, clearer API |
| Protocol vs ABC | `Protocol` | Loose coupling, custom platforms don't inherit from core |
| Inheritance vs composition | Composition (Protocol interface) | Serialization-friendly, extensible |
| URL evolution | Lenient parsing, `handles_hostname()` | URLs change, typed class = entity not format |
| Platform identifier | `str` in Protocol, `Literal` in classes | Extensibility for custom platforms |
| Canonical URL | Dropped | Simplicity, derivable if needed |
| Special links (mailto, tel) | Keep as special case | Useful for scraping, not a "platform" |
| Backwards compat | Keep `Extraction` wrapper | 0.x users can migrate gradually |
| Hostname matching | `handles_hostname()` method | Flexibility for dynamic platforms (Mastodon) |
| State management | `Extractor` class + module-level API | Like requests/httpx: simple default, custom when needed |
| Result wrapping | `Extraction` object with helper methods | Ergonomic grouping/filtering, 0.x compatibility |
| Error handling | Return `None` by default, optional `strict=True` | Lenient parsing suits scraping use cases |
| Immutability | `frozen=True` Pydantic models | Hashable, safe to use in sets/dicts |
| Hashing | `__hash__` uses `url` string | URL is the unique identifier |

## Custom Platforms

Third parties can add platforms without modifying core:

```python
from pydantic import BaseModel
from typing import Literal
import socials

class MastodonProfileURL(BaseModel, frozen=True):
    url: str
    platform: Literal["mastodon"] = "mastodon"
    entity_type: Literal["profile"] = "profile"
    instance: str
    username: str

    def __hash__(self) -> int:
        return hash(self.url)

    def get_parent(self) -> None:
        return None

    def get_root(self) -> "MastodonProfileURL":
        return self

    def get_ancestors(self) -> "list[SocialsURL]":
        return []


class MastodonParser:
    platform = "mastodon"

    def handles_hostname(self, hostname: str) -> bool:
        # Check known instances or verify dynamically
        return hostname in ["mastodon.social", "fosstodon.org", ...]

    def parse(self, url: str) -> MastodonProfileURL | None:
        # Custom parsing logic
        ...

# Register with socials
socials.register(MastodonParser())
```
