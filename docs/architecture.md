# Architecture Overview

This document describes the high-level architecture of socials 1.0.

## Use Cases

Social URLs are more than just profiles. They can be posts, repos, issues, videos, playlists, and more. This library addresses the following use cases:

1. **Entity detection** - What kind of thing is this URL? (profile, repo, issue, tweet, video)
2. **Identifier extraction** - Get the username, repo slug, issue number, video ID, etc.
3. **Parent relationships** - Navigate hierarchy (issue -> repo -> profile)
4. **Filtering by platform or type** - "Give me only GitHub profiles from this list"
5. **Batch extraction** - Process a list of scraped URLs, group by platform

## Package Structure

```
socials/
├── __init__.py          # Public API facade
├── protocols.py         # SocialsURL and PlatformParser protocols
├── registry.py          # Domain -> parser registry
├── extractor.py         # Extractor class and Extraction result object
├── cli.py               # Command-line interface
└── platforms/
    ├── __init__.py      # DEFAULT_PARSERS dict
    ├── base.py          # URL utilities (extract_hostname, path parsing)
    ├── github.py        # GitHubParser + URL types
    ├── twitter.py       # TwitterParser + URL types
    ├── linkedin.py      # LinkedInParser + URL types
    ├── youtube.py       # YouTubeParser + URL types
    ├── facebook.py      # FacebookParser + URL types
    ├── instagram.py     # InstagramParser + URL types
    └── misc.py          # EmailParser, PhoneParser + URL types
```

## Component Interaction

```
┌─────────────────────────────────────────────────────────┐
│              Extractor (or module-level API)            │
│                                                         │
│  socials.parse(url)                                     │
│  socials.parse_all(urls) -> Extraction                  │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│                      Registry                           │
│                                                         │
│  extract_hostname(url) -> lookup parser                 │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│                   Platform Parser                       │
│                                                         │
│  GitHubParser.parse(url) -> GitHubRepoURL               │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│        Typed URL (implements SocialsURL Protocol)       │
│                                                         │
│  GitHubRepoURL {url, platform, entity_type, owner, ...} │
│                                                         │
│  .get_parent() -> GitHubProfileURL | None               │
│  .get_root() -> GitHubProfileURL                        │
│  .get_ancestors() -> list[SocialsURL]                   │
└─────────────────────────────────────────────────────────┘
```

**Flow:**

1. User calls `socials.parse(url)`
2. Registry extracts domain from URL and looks up the responsible parser
3. Parser matches URL against its patterns and returns a typed URL object
4. Typed URL implements the `SocialsURL` protocol with hierarchy traversal

## Components

For detailed documentation on each component:

- [Parsers](parsers.md) - Platform-specific URL parsers and the PlatformParser protocol
- [Registry](registry.md) - URL routing and parser registration
- [URLs](urls.md) - Typed URL objects and the SocialsURL protocol
- [Extraction](extraction.md) - Extractor class and Extraction result container

## Design Principles

- **Typed classes over dicts** - URL objects are typed Pydantic models for IDE support and type safety
- **Protocols over inheritance** - Custom platforms implement a protocol, not inherit from a base class
- **Lenient parsing** - Unrecognized URLs return `None` by default (suitable for scraping)
- **Immutable results** - URL objects are frozen and hashable
- **Backwards compatible** - 0.x API methods are deprecated but still work
