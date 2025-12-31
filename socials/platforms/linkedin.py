"""LinkedIn platform parser and URL types."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, ClassVar, Literal

from pydantic import BaseModel

if TYPE_CHECKING:
    from socials.protocols import SocialsURL

# Regex patterns with named groups
# Adapted from: https://github.com/lorey/social-media-profiles-regexs
PROFILE_REGEX = re.compile(
    r"^https?://(?:[\w]+\.)?linkedin\.com/in/(?P<username>[\w\-_]+)/?$",
)
PROFILE_PUB_REGEX = re.compile(
    r"^https?://(?:[\w]+\.)?linkedin\.com/pub/(?P<username>[A-Za-z0-9_-]+)"
    r"(?:/[A-Za-z0-9]+){3}/?$",
)
COMPANY_REGEX = re.compile(
    r"^https?://(?:[\w]+\.)?linkedin\.com/(?:company|school)/"
    r"(?P<company_id>[A-Za-z0-9_-]+)/?$",
)


class LinkedInProfileURL(BaseModel, frozen=True):
    """LinkedIn personal profile URL."""

    url: str
    platform: Literal["linkedin"] = "linkedin"
    entity_type: Literal["profile"] = "profile"
    username: str

    def __hash__(self) -> int:
        """Return hash based on URL."""
        return hash(self.url)

    def get_parent(self) -> None:
        """Return parent (None for profiles)."""
        return

    def get_root(self) -> LinkedInProfileURL:
        """Return root of hierarchy (self for profiles)."""
        return self

    def get_ancestors(self) -> list[SocialsURL]:
        """Return ancestors (empty for profiles)."""
        return []


class LinkedInCompanyURL(BaseModel, frozen=True):
    """LinkedIn company page URL."""

    url: str
    platform: Literal["linkedin"] = "linkedin"
    entity_type: Literal["company"] = "company"
    company_id: str

    def __hash__(self) -> int:
        """Return hash based on URL."""
        return hash(self.url)

    def get_parent(self) -> None:
        """Return parent (None for companies)."""
        return

    def get_root(self) -> LinkedInCompanyURL:
        """Return root of hierarchy (self for companies)."""
        return self

    def get_ancestors(self) -> list[SocialsURL]:
        """Return ancestors (empty for companies)."""
        return []


class LinkedInParser:
    """Parser for LinkedIn URLs."""

    platform = "linkedin"
    schemes: ClassVar[set[str]] = {"http", "https"}

    def handles_hostname(self, hostname: str) -> bool:
        """Check if this parser handles the given hostname."""
        # LinkedIn has various subdomains (www, de, uk, etc.)
        return hostname == "linkedin.com" or hostname.endswith(".linkedin.com")

    def parse(self, url: str) -> LinkedInProfileURL | LinkedInCompanyURL | None:
        """Parse a LinkedIn URL into a typed object."""
        # Try company first (more specific path)
        if match := COMPANY_REGEX.match(url):
            return LinkedInCompanyURL(url=url, **match.groupdict())

        # Try /in/ profile
        if match := PROFILE_REGEX.match(url):
            return LinkedInProfileURL(url=url, **match.groupdict())

        # Legacy public profile format
        if match := PROFILE_PUB_REGEX.match(url):
            return LinkedInProfileURL(url=url, **match.groupdict())

        return None
