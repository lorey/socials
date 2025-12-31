"""Extractor and Extraction classes for socials."""

from __future__ import annotations

import warnings
from collections import defaultdict
from typing import TYPE_CHECKING

from socials.platforms import DEFAULT_PARSERS
from socials.platforms.misc import EmailURL
from socials.protocols import ParseError
from socials.registry import Registry

if TYPE_CHECKING:
    from socials.protocols import SocialsURL


class Extraction:
    """Result of extracting social URLs from a list of URLs."""

    def __init__(self, results: list[SocialsURL]) -> None:
        """Initialize with parsed URL results.

        Args:
            results: List of parsed SocialsURL objects.

        """
        self._results = results

    def all(self) -> list[SocialsURL]:
        """Return all parsed URLs.

        Returns:
            List of all SocialsURL objects.

        """
        return list(self._results)

    def by_platform(self) -> dict[str, list[SocialsURL]]:
        """Group results by platform.

        Returns:
            Dictionary mapping platform names to lists of URLs.

        """
        grouped: dict[str, list[SocialsURL]] = defaultdict(list)
        for result in self._results:
            grouped[result.platform].append(result)
        return dict(grouped)

    def by_type(self) -> dict[str, list[SocialsURL]]:
        """Group results by entity type.

        Returns:
            Dictionary mapping entity types to lists of URLs.

        """
        grouped: dict[str, list[SocialsURL]] = defaultdict(list)
        for result in self._results:
            grouped[result.entity_type].append(result)
        return dict(grouped)

    # 0.x backwards compatibility methods (deprecated)

    def _get_compat_url(self, url_obj: SocialsURL) -> str:
        """Get URL string for backwards compat (applies cleaning like 0.x)."""
        if isinstance(url_obj, EmailURL):
            return url_obj.email
        return url_obj.url

    def get_matches_per_platform(self) -> dict[str, list[str]]:
        """Get URL strings grouped by platform.

        .. deprecated:: 1.0
            Use :meth:`by_platform` instead, which returns typed URL objects.

        Returns:
            Dictionary mapping platform names to lists of URL strings.

        """
        warnings.warn(
            "get_matches_per_platform() is deprecated, use by_platform() instead",
            DeprecationWarning,
            stacklevel=2,
        )
        result: dict[str, list[str]] = defaultdict(list)
        for url_obj in self._results:
            result[url_obj.platform].append(self._get_compat_url(url_obj))
        return dict(result)

    def get_matches_for_platform(self, platform: str) -> list[str]:
        """Get URL strings for a specific platform.

        .. deprecated:: 1.0
            Use :meth:`by_platform` instead, which returns typed URL objects.

        Args:
            platform: Platform name to filter by.

        Returns:
            List of URL strings for the given platform.

        """
        warnings.warn(
            "get_matches_for_platform() is deprecated, "
            "use by_platform()[platform] instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return [
            self._get_compat_url(url_obj)
            for url_obj in self._results
            if url_obj.platform == platform
        ]


class Extractor:
    """Extractor for parsing social URLs."""

    def __init__(
        self,
        *,
        platforms: list[str] | None = None,
        strict: bool = False,
    ) -> None:
        """Initialize the extractor.

        Args:
            platforms: If provided, only include these platforms.
            strict: If True, raise ParseError for unrecognized URLs.

        """
        self._strict = strict
        self._registry = Registry()

        if platforms is None:
            platforms = list(DEFAULT_PARSERS.keys())

        for platform in platforms:
            try:
                parser = DEFAULT_PARSERS[platform]
            except KeyError:
                msg = f"Unknown platform: {platform}"
                raise ValueError(msg) from None
            self._registry.register(parser)

    def parse(self, url: str) -> SocialsURL | None:
        """Parse a single URL.

        Args:
            url: URL to parse.

        Returns:
            Parsed SocialsURL object, or None if not recognized.

        Raises:
            ParseError: If strict mode is enabled and URL is not recognized.

        """
        result = self._registry.parse(url)

        if result is None and self._strict:
            msg = f"Unrecognized URL: {url}"
            raise ParseError(msg)

        return result

    def extract(self, urls: list[str]) -> Extraction:
        """Parse multiple URLs.

        Args:
            urls: List of URLs to parse.

        Returns:
            Extraction object containing parsed results.

        """
        results: list[SocialsURL] = []
        for url in urls:
            result = self.parse(url)
            if result is not None:
                results.append(result)
        return Extraction(results)
