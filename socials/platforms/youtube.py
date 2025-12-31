"""YouTube platform parser and URL types."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, ClassVar, Literal, Optional

from pydantic import BaseModel

if TYPE_CHECKING:
    from socials.protocols import SocialsURL

# Regex patterns with named groups
# Adapted from: https://github.com/lorey/social-media-profiles-regexs
CHANNEL_ID_REGEX = re.compile(
    r"^https?://(?:www\.|m\.)?youtube\.com/channel/(?P<channel_id>UC[A-Za-z0-9_-]+)/?$",
)
USER_REGEX = re.compile(
    r"^https?://(?:www\.|m\.)?youtube\.com/user/(?P<username>[A-Za-z0-9_.-]+)/?$",
)
CUSTOM_REGEX = re.compile(
    r"^https?://(?:www\.|m\.)?youtube\.com/c/(?P<custom_url>[A-Za-z0-9_.-]+)/?$",
)
HANDLE_REGEX = re.compile(
    r"^https?://(?:www\.|m\.)?youtube\.com/@(?P<custom_url>[A-Za-z0-9_.-]+)/?$",
)
# Direct /channelname format (excluding reserved paths)
_RESERVED = (
    "about|account|channel|embed|feed|gaming|hashtag|live|music|"
    "playlist|premium|redirect|results|shorts|trending|upload|watch|c|user"
)
DIRECT_REGEX = re.compile(
    rf"^https?://(?:www\.|m\.)?youtube\.com/(?P<custom_url>(?!{_RESERVED})[A-Za-z0-9_.-]+)/?$",
)


class YouTubeChannelURL(BaseModel, frozen=True):
    """YouTube channel URL."""

    url: str
    platform: Literal["youtube"] = "youtube"
    entity_type: Literal["channel"] = "channel"
    channel_id: Optional[str] = None
    username: Optional[str] = None
    custom_url: Optional[str] = None

    def __hash__(self) -> int:
        """Return hash based on URL."""
        return hash(self.url)

    def get_parent(self) -> None:
        """Return parent (None for channels)."""
        return

    def get_root(self) -> YouTubeChannelURL:
        """Return root of hierarchy (self for channels)."""
        return self

    def get_ancestors(self) -> list[SocialsURL]:
        """Return ancestors (empty for channels)."""
        return []


class YouTubeParser:
    """Parser for YouTube URLs."""

    platform = "youtube"
    schemes: ClassVar[set[str]] = {"http", "https"}

    def handles_hostname(self, hostname: str) -> bool:
        """Check if this parser handles the given hostname."""
        return hostname in {
            "youtube.com",
            "www.youtube.com",
            "m.youtube.com",
        }

    def parse(self, url: str) -> YouTubeChannelURL | None:
        """Parse a YouTube URL into a typed object."""
        if match := CHANNEL_ID_REGEX.match(url):
            return YouTubeChannelURL(url=url, **match.groupdict())

        if match := USER_REGEX.match(url):
            return YouTubeChannelURL(url=url, **match.groupdict())

        if match := CUSTOM_REGEX.match(url):
            return YouTubeChannelURL(url=url, **match.groupdict())

        if match := HANDLE_REGEX.match(url):
            return YouTubeChannelURL(url=url, **match.groupdict())

        if match := DIRECT_REGEX.match(url):
            return YouTubeChannelURL(url=url, **match.groupdict())

        return None
