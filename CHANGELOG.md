# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2025-12-31

### Added

- **Typed URL classes**: Parse URLs into typed objects like `GitHubRepoURL`, `TwitterProfileURL`, etc.
- **Entity type detection**: Each URL now has an `entity_type` field (profile, repo, channel, company, email, phone)
- **Hierarchy navigation**: `get_parent()`, `get_root()`, `get_ancestors()` methods for traversing URL hierarchies
- **New extraction methods**: `extraction.all()`, `extraction.by_platform()`, `extraction.by_type()`
- **Extractor class**: Create custom extractors with platform filtering and strict mode
- **Strict mode**: Optionally raise `ParseError` for unrecognized URLs
- **Protocol-based architecture**: `SocialsURL` and `PlatformParser` protocols for extensibility
- **Phone number support**: Parse `tel:` URLs
- **Pydantic models**: All URL types are immutable, hashable Pydantic models

### Changed

- Complete internal rewrite to typed architecture
- `socials.parse()` now returns typed objects instead of strings
- `socials.extract()` returns an `Extraction` object with new methods

### Deprecated

- `get_matches_per_platform()` - use `by_platform()` instead
- `get_matches_for_platform()` - use `by_platform()[platform]` instead

## [0.3.0] - 2025-12-30

### Added

- Support for Instagram URLs
- Support for YouTube URLs
- Support for Facebook profile.php URLs (profile ID-based)
- CLI with `check` and `extract` commands
- Type hints throughout the codebase
- Support for Python 3.9-3.13

### Changed

- Modernized packaging and CI/CD (pyproject.toml, GitHub Actions, MkDocs)

### Fixed

- Regex patterns now use proper anchors for exact matching

### Removed

- Dropped support for Python 3.4-3.8

## [0.2.0] - 2018-05-31

### Added

- Email address extraction
- Extraction of specific platforms via `get_matches_for_platform()`

## [0.1.0] - 2018-05-18

### Added

- First release on PyPI
- Support for Facebook, Twitter, LinkedIn, GitHub detection

[Unreleased]: https://github.com/lorey/socials/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/lorey/socials/compare/v0.3.0...v1.0.0
[0.3.0]: https://github.com/lorey/socials/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/lorey/socials/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/lorey/socials/releases/tag/v0.1.0
