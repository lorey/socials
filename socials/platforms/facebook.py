"""Facebook platform parser and URL types."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, ClassVar, Literal

from pydantic import BaseModel

if TYPE_CHECKING:
    from socials.protocols import SocialsURL

# Regex patterns with named groups
# Adapted from: https://github.com/lorey/social-media-profiles-regexs
PROFILE_REGEX = re.compile(
    r"^https?://(?:www\.)?(?:facebook|fb)\.com/"
    r"(?P<username>(?![A-Za-z]+\.php)"
    r"(?!marketplace|gaming|watch|me|messages|help|search|groups)[A-Za-z0-9_.-]+)/?$",
)
PROFILE_BY_ID_REGEX = re.compile(
    r"^https?://(?:www\.)?facebook\.com/(?:profile\.php\?id=)?(?P<user_id>[0-9]+)$",
)


class FacebookProfileURL(BaseModel, frozen=True):
    """Facebook user or page profile URL."""

    url: str
    platform: Literal["facebook"] = "facebook"
    entity_type: Literal["profile"] = "profile"
    username: str | None = None
    user_id: str | None = None

    def __hash__(self) -> int:
        """Return hash based on URL."""
        return hash(self.url)

    def get_parent(self) -> None:
        """Return parent (None for profiles)."""
        return

    def get_root(self) -> FacebookProfileURL:
        """Return root of hierarchy (self for profiles)."""
        return self

    def get_ancestors(self) -> list[SocialsURL]:
        """Return ancestors (empty for profiles)."""
        return []


class FacebookParser:
    """Parser for Facebook URLs."""

    platform = "facebook"
    schemes: ClassVar[set[str]] = {"http", "https"}

    def handles_hostname(self, hostname: str) -> bool:
        """Check if this parser handles the given hostname."""
        return hostname in {
            "facebook.com",
            "www.facebook.com",
            "fb.com",
            "www.fb.com",
            "m.facebook.com",
        }

    def parse(self, url: str) -> FacebookProfileURL | None:
        """Parse a Facebook URL into a typed object."""
        # Try profile by ID first (more specific)
        if match := PROFILE_BY_ID_REGEX.match(url):
            return FacebookProfileURL(url=url, **match.groupdict())

        # Try username profile
        if match := PROFILE_REGEX.match(url):
            return FacebookProfileURL(url=url, **match.groupdict())

        return None
