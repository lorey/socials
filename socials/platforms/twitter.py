"""Twitter/X platform parser and URL types."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, ClassVar, Literal

from pydantic import BaseModel

if TYPE_CHECKING:
    from socials.protocols import SocialsURL

# Regex patterns with named groups
# Adapted from: https://github.com/lorey/social-media-profiles-regexs
PROFILE_REGEX = re.compile(
    r"^https?://(?:www\.|mobile\.)?(?:twitter|x)\.com/"
    r"@?(?!home|share|privacy|tos|explore|search|settings|messages|i|login|compose)"
    r"(?P<username>[A-Za-z0-9_]{1,15})/?$",
)


class TwitterProfileURL(BaseModel, frozen=True):
    """Twitter/X user profile URL."""

    url: str
    platform: Literal["twitter"] = "twitter"
    entity_type: Literal["profile"] = "profile"
    username: str

    def __hash__(self) -> int:
        """Return hash based on URL."""
        return hash(self.url)

    def get_parent(self) -> None:
        """Return parent (None for profiles)."""
        return

    def get_root(self) -> TwitterProfileURL:
        """Return root of hierarchy (self for profiles)."""
        return self

    def get_ancestors(self) -> list[SocialsURL]:
        """Return ancestors (empty for profiles)."""
        return []


class TwitterParser:
    """Parser for Twitter/X URLs."""

    platform = "twitter"
    schemes: ClassVar[set[str]] = {"http", "https"}

    def handles_hostname(self, hostname: str) -> bool:
        """Check if this parser handles the given hostname."""
        return hostname in {
            "twitter.com",
            "www.twitter.com",
            "x.com",
            "www.x.com",
            "mobile.twitter.com",
            "mobile.x.com",
        }

    def parse(self, url: str) -> TwitterProfileURL | None:
        """Parse a Twitter/X URL into a typed object."""
        if match := PROFILE_REGEX.match(url):
            return TwitterProfileURL(url=url, **match.groupdict())
        return None
