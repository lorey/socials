# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Support for Instagram URLs
- Support for YouTube URLs
- Support for Facebook profile.php URLs (profile ID-based)
- CLI with `check` and `extract` commands using typer
- Type hints throughout the codebase
- GitHub Actions CI/CD with trusted publishing
- Support for Python 3.9-3.13

### Changed

- Migrated from setup.py to pyproject.toml with hatch-vcs
- Replaced flake8 with ruff for linting and formatting
- Replaced Sphinx with MkDocs for documentation
- Minimum Python version is now 3.9

### Fixed

- Regex patterns now use proper anchors (`^`/`$`) for exact matching
- Character classes use `[A-Za-z]` instead of `[A-z]` (avoids matching `[\]^_``)

### Removed

- Dropped support for Python 3.4-3.8
- Removed Travis CI (replaced with GitHub Actions)
- Removed tox (using uv + GitHub Actions matrix)

## [0.2.0] - 2018-05-31

### Added

- Email address extraction
- Extraction of specific platforms via `get_matches_for_platform()`

## [0.1.0] - 2018-05-18

### Added

- First release on PyPI
- Support for Facebook, Twitter, LinkedIn, GitHub detection

[Unreleased]: https://github.com/lorey/socials/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/lorey/socials/compare/0.1.0...v0.2.0
[0.1.0]: https://github.com/lorey/socials/releases/tag/0.1.0
