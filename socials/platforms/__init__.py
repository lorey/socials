"""Platform parsers for socials."""

from __future__ import annotations

from typing import TYPE_CHECKING

from socials.platforms.facebook import FacebookParser
from socials.platforms.github import GitHubParser
from socials.platforms.instagram import InstagramParser
from socials.platforms.linkedin import LinkedInParser
from socials.platforms.misc import EmailParser, PhoneParser
from socials.platforms.twitter import TwitterParser
from socials.platforms.youtube import YouTubeParser

if TYPE_CHECKING:
    from socials.protocols import PlatformParser

# Default parsers by platform name
DEFAULT_PARSERS: dict[str, PlatformParser] = {
    GitHubParser.platform: GitHubParser(),
    TwitterParser.platform: TwitterParser(),
    LinkedInParser.platform: LinkedInParser(),
    FacebookParser.platform: FacebookParser(),
    InstagramParser.platform: InstagramParser(),
    YouTubeParser.platform: YouTubeParser(),
    EmailParser.platform: EmailParser(),
    PhoneParser.platform: PhoneParser(),
}

__all__ = [
    "DEFAULT_PARSERS",
    "EmailParser",
    "FacebookParser",
    "GitHubParser",
    "InstagramParser",
    "LinkedInParser",
    "PhoneParser",
    "TwitterParser",
    "YouTubeParser",
]
