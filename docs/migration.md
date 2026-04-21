# Migration Guide

This guide helps you migrate from socials 0.x to 1.x.

## Overview

Version 1.0 introduces a new typed API while maintaining backwards compatibility with 0.x. The old API is deprecated and will be removed in a future version.

## API Changes

### Module-level functions

| 0.x (deprecated) | 1.x |
|------------------|-----|
| `socials.extract(urls)` | `socials.parse_all(urls)` |

```python notest
import socials

# 0.x - deprecated
socials.extract(["https://github.com/lorey"])

# 1.x - use instead
socials.parse_all(["https://github.com/lorey"])
```

### Extraction methods

| 0.x (deprecated) | 1.x |
|------------------|-----|
| `extraction.get_matches_per_platform()` | `extraction.by_platform()` |
| `extraction.get_matches_for_platform(p)` | `extraction.by_platform()[p]` |

The deprecated methods return URL strings, while the new methods return typed `SocialsURL` objects:

```python notest
import socials

extraction = socials.parse_all(["https://github.com/lorey"])

# 0.x - deprecated (returns strings)
extraction.get_matches_per_platform()
extraction.get_matches_for_platform("github")

# 1.x - use instead (returns typed objects)
extraction.by_platform()
extraction.by_platform()["github"]
```

## Deprecation Warnings

All deprecated methods emit `DeprecationWarning`. To see these warnings, run Python with `-W default`:

```bash
python -W default your_script.py
```
