"""Registry for platform parsers."""

from __future__ import annotations

from typing import TYPE_CHECKING

from socials.platforms.base import extract_hostname, extract_scheme

if TYPE_CHECKING:
    from socials.protocols import PlatformParser, SocialsURL


class Registry:
    """Registry that maps hostnames to platform parsers."""

    def __init__(self, parsers: list[PlatformParser] | None = None) -> None:
        """Initialize registry with optional list of parsers.

        Args:
            parsers: List of platform parsers to register.

        """
        self._parsers: list[PlatformParser] = list(parsers) if parsers else []

    def register(self, parser: PlatformParser) -> None:
        """Register a new parser.

        Args:
            parser: Parser to register.

        """
        self._parsers.append(parser)

    def get_parser_for_url(self, url: str) -> PlatformParser | None:
        """Find the parser that handles the given URL.

        Args:
            url: URL to find parser for.

        Returns:
            Parser that handles the URL, or None.

        """
        scheme = extract_scheme(url)

        if scheme in ("http", "https"):
            hostname = extract_hostname(url)
            return self.get_parser_for_hostname(hostname)

        if scheme:
            return self.get_parser_for_scheme(scheme)

        # No scheme (e.g., raw email) - try all parsers
        for parser in self._parsers:
            if parser.parse(url) is not None:
                return parser
        return None

    def get_parser_for_scheme(self, scheme: str) -> PlatformParser | None:
        """Find the parser that handles the given URL scheme.

        Args:
            scheme: URL scheme to find parser for (e.g., 'mailto', 'tel').

        Returns:
            Parser that handles the scheme, or None.

        """
        for parser in self._parsers:
            if scheme in parser.schemes:
                return parser
        return None

    def get_parser_for_hostname(self, hostname: str) -> PlatformParser | None:
        """Find the parser that handles the given hostname.

        Args:
            hostname: Hostname to find parser for.

        Returns:
            Parser that handles the hostname, or None.

        """
        for parser in self._parsers:
            if parser.handles_hostname(hostname):
                return parser
        return None

    def parse(self, url: str) -> SocialsURL | None:
        """Parse a URL using the appropriate parser.

        Args:
            url: URL to parse.

        Returns:
            Parsed URL object, or None if no parser handles it.

        """
        parser = self.get_parser_for_url(url)
        if parser is None:
            return None
        return parser.parse(url)

    @property
    def parsers(self) -> list[PlatformParser]:
        """Return list of registered parsers."""
        return list(self._parsers)
