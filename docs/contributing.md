# Contributing

Guide for contributing to socials development.

## Development Setup

Clone the repository and install dev dependencies:

```bash
git clone https://github.com/lorey/socials.git
cd socials

python -m venv venv
source venv/bin/activate

pip install -e ".[dev]"
```

Or with uv:

```bash
uv sync --extra dev
```

## Running Tests

```bash
pytest

pytest --cov=socials --cov-report=html
```

## Linting and Formatting

We use ruff for linting and formatting:

```bash
ruff check .

ruff check --fix .

ruff format .
```

## Type Checking

```bash
mypy socials
```

## Adding a New Platform

1. **Create URL classes** in `socials/platforms/yourplatform.py`:

```
from typing import ClassVar, Literal
from pydantic import BaseModel

class YourPlatformProfileURL(BaseModel, frozen=True):
    url: str
    platform: Literal["yourplatform"] = "yourplatform"
    entity_type: Literal["profile"] = "profile"
    username: str

    def __hash__(self) -> int:
        return hash(self.url)

    def get_parent(self) -> None:
        return None

    def get_root(self) -> YourPlatformProfileURL:
        return self

    def get_ancestors(self) -> list:
        return []
```

2. **Create the parser**:

```
import re

PROFILE_REGEX = re.compile(
    r"^https?://(?:www\.)?yourplatform\.com/(?P<username>[A-Za-z0-9_]+)/?$"
)

class YourPlatformParser:
    platform = "yourplatform"
    schemes: ClassVar[set[str]] = {"http", "https"}

    def handles_hostname(self, hostname: str) -> bool:
        return hostname in {"yourplatform.com", "www.yourplatform.com"}

    def parse(self, url: str) -> YourPlatformProfileURL | None:
        if match := PROFILE_REGEX.match(url):
            return YourPlatformProfileURL(url=url, **match.groupdict())
        return None
```

3. **Register the parser** in `socials/platforms/__init__.py`:

```
from socials.platforms.yourplatform import YourPlatformParser

DEFAULT_PARSERS: dict[str, PlatformParser] = {
    # ... existing parsers ...
    "yourplatform": YourPlatformParser(),
}
```

4. **Add tests** in `tests/test_yourplatform.py`:

```python
import socials

def test_yourplatform_profile():
    url = socials.parse("https://yourplatform.com/username")
    assert url is not None
    assert url.platform == "yourplatform"
    assert url.entity_type == "profile"
    assert url.username == "username"
```

5. **Run tests and linting** to verify everything works.

## Regex Conventions

- Use `^` and `$` anchors for exact matching
- Use non-capturing groups `(?:...)` for optional parts
- Use named capture groups `(?P<name>...)` for extracted values
- Character classes should use `[A-Za-z0-9_-]` (avoiding chars between Z and a)
- Optional trailing slash: `/?$`
- Optional https: `https?://`
- Optional www: `(?:www\.)?`

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Typed classes vs generic dict | Typed classes | Type safety, IDE support, clearer API |
| Protocol vs ABC | Protocol | Loose coupling, custom platforms don't inherit from core |
| URL evolution | Lenient parsing | URLs change, typed class represents entity not format |
| Error handling | Return `None` by default | Lenient parsing suits scraping use cases |
| Immutability | `frozen=True` Pydantic models | Hashable, safe to use in sets/dicts |
| Backwards compat | Keep `Extraction` wrapper | 0.x users can migrate gradually |

## Pull Request Guidelines

1. Fork the repository
2. Create a feature branch
3. Write tests for new functionality
4. Ensure all tests pass and linting is clean
5. Submit a pull request with a clear description

## Releasing

Releases are managed by maintainers:

```bash
git tag v1.2.3
git push --tags
```

The CI/CD pipeline handles PyPI publishing automatically on tagged commits.
