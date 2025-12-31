"""Instagram platform parser and URL types."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, ClassVar, Literal

from pydantic import BaseModel

if TYPE_CHECKING:
    from socials.protocols import SocialsURL

# Regex patterns with named groups
# Adapted from: https://github.com/lorey/social-media-profiles-regexs
PROFILE_REGEX = re.compile(
    r"^https?://(?:www\.)?(?:instagram\.com|instagr\.am)/"
    r"(?!about|accounts|direct|explore|legal|p|privacy|reels|stories|tv)"
    r"(?P<username>[A-Za-z0-9_.]{1,30})/?$",
)


class InstagramProfileURL(BaseModel, frozen=True):
    """Instagram user profile URL."""

    url: str
    platform: Literal["instagram"] = "instagram"
    entity_type: Literal["profile"] = "profile"
    username: str

    def __hash__(self) -> int:
        """Return hash based on URL."""
        return hash(self.url)

    def get_parent(self) -> None:
        """Return parent (None for profiles)."""
        return

    def get_root(self) -> InstagramProfileURL:
        """Return root of hierarchy (self for profiles)."""
        return self

    def get_ancestors(self) -> list[SocialsURL]:
        """Return ancestors (empty for profiles)."""
        return []


class InstagramParser:
    """Parser for Instagram URLs."""

    platform = "instagram"
    schemes: ClassVar[set[str]] = {"http", "https"}

    def handles_hostname(self, hostname: str) -> bool:
        """Check if this parser handles the given hostname."""
        return hostname in {
            "instagram.com",
            "www.instagram.com",
            "instagr.am",
            "www.instagr.am",
        }

    def parse(self, url: str) -> InstagramProfileURL | None:
        """Parse an Instagram URL into a typed object."""
        if match := PROFILE_REGEX.match(url):
            return InstagramProfileURL(url=url, **match.groupdict())
        return None
