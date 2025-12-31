"""Top-level package for Socials.

Social Account Detection and Extraction for Python.
"""

from __future__ import annotations

from importlib.metadata import version

from socials.extractor import Extraction, Extractor
from socials.protocols import ParseError, PlatformParser, SocialsURL

__version__ = version("socials")

# Default extractor instance for module-level API
_default_extractor = Extractor()


def parse(url: str) -> SocialsURL | None:
    """Parse a single URL into a typed object.

    Args:
        url: URL to parse.

    Returns:
        Parsed SocialsURL object, or None if not recognized.

    Example:
        >>> result = socials.parse("https://github.com/lorey/socials")
        >>> result.platform
        'github'
        >>> result.entity_type
        'repo'

    """
    return _default_extractor.parse(url)


def extract(urls: list[str]) -> Extraction:
    """Parse multiple URLs and return an Extraction result.

    Args:
        urls: List of URLs to parse.

    Returns:
        Extraction object with helper methods for grouping/filtering.

    Example:
        >>> extraction = socials.extract(urls)
        >>> extraction.by_platform()
        {'github': [...], 'twitter': [...]}

    """
    return _default_extractor.extract(urls)


__all__ = [
    # Classes
    "Extraction",
    "Extractor",
    "ParseError",
    "PlatformParser",
    "SocialsURL",
    # Metadata
    "__version__",
    # Functions
    "extract",
    "parse",
]
