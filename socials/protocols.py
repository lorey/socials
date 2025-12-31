"""Protocol definitions for socials."""

from __future__ import annotations

from typing import ClassVar, Protocol, runtime_checkable


class ParseError(Exception):
    """Raised when URL parsing fails (if strict mode enabled)."""


@runtime_checkable
class SocialsURL(Protocol):
    """Common interface all parsed URLs implement."""

    @property
    def url(self) -> str:
        """Original URL string."""
        ...

    @property
    def platform(self) -> str:
        """Platform identifier (e.g., 'github', 'twitter')."""
        ...

    @property
    def entity_type(self) -> str:
        """Entity type (e.g., 'profile', 'repo')."""
        ...

    def get_parent(self) -> SocialsURL | None:
        """Return immediate parent (issue → repo)."""
        ...

    def get_root(self) -> SocialsURL:
        """Return top of hierarchy (issue → profile/org)."""
        ...

    def get_ancestors(self) -> list[SocialsURL]:
        """Return full chain from parent to root: [repo, profile]."""
        ...


@runtime_checkable
class PlatformParser(Protocol):
    """Interface for platform-specific URL parsers."""

    platform: str
    schemes: ClassVar[set[str]]

    def handles_hostname(self, hostname: str) -> bool:
        """Check if this parser handles the given hostname."""
        ...

    def parse(self, url: str) -> SocialsURL | None:
        """Parse URL into typed object, or None if not recognized."""
        ...
