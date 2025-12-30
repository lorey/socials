# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/lorey/socials/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/lorey/socials/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/lorey/socials/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/lorey/socials/releases/tag/v0.1.0
