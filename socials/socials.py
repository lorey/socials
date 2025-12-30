"""Main module."""

from __future__ import annotations

import re
from collections.abc import Callable

PLATFORM_FACEBOOK = "facebook"
PLATFORM_GITHUB = "github"
PLATFORM_LINKEDIN = "linkedin"
PLATFORM_TWITTER = "twitter"
PLATFORM_INSTAGRAM = "instagram"
PLATFORM_YOUTUBE = "youtube"
PLATFORM_EMAIL = "email"

FACEBOOK_URL_REGEXS = [
    r"^http(s)?://(www\.)?(facebook|fb)\.com/[A-Za-z0-9_\-\.]+/?$",
    r"^http(s)?://(www\.)?(facebook|fb)\.com/profile\.php\?id=\d+$",
]

GITHUB_URL_REGEXS = [
    r"^http(s)?://(www\.)?github\.com/[A-Za-z0-9_-]+/?$",
]

LINKEDIN_URL_REGEXS = [
    # private
    r"^http(s)?://([\w]+\.)?linkedin\.com/in/[A-Za-z0-9_-]+/?$",
    r"^http(s)?://([\w]+\.)?linkedin\.com/pub/[A-Za-z0-9_-]+(\/[A-z 0-9]+){3}/?$",
    # companies
    r"^http(s)?://(www\.)?linkedin\.com/company/[A-Za-z0-9_-]+/?$",
]

TWITTER_URL_REGEXS = [
    r"^http(s)?://(.*\.)?twitter\.com\/[A-Za-z0-9_]+/?$",
]

INSTAGRAM_URL_REGEXS = [
    r"^http(s)?://(www\.)?instagram\.com/[A-Za-z0-9_.]+/?$",
    r"^http(s)?://(www\.)?instagr\.am/[A-Za-z0-9_.]+/?$",
]

YOUTUBE_URL_REGEXS = [
    r"^http(s)?://(www\.)?youtube\.com/user/[A-z0-9_.-]+/?$",
    r"^http(s)?://(www\.)?youtube\.com/c/[A-z0-9_.-]+/?$",
    r"^http(s)?://(www\.)?youtube\.com/[A-z0-9_.-]+/?$",
]

EMAIL_REGEX = r"^(mailto:)?[\w\.-]+@[\w\.-]+$"


PATTERNS = {
    PLATFORM_FACEBOOK: FACEBOOK_URL_REGEXS,
    PLATFORM_TWITTER: TWITTER_URL_REGEXS,
    PLATFORM_LINKEDIN: LINKEDIN_URL_REGEXS,
    PLATFORM_GITHUB: GITHUB_URL_REGEXS,
    PLATFORM_INSTAGRAM: INSTAGRAM_URL_REGEXS,
    PLATFORM_YOUTUBE: YOUTUBE_URL_REGEXS,
    PLATFORM_EMAIL: [EMAIL_REGEX],
}

ERROR_MSG_UNKNOWN_PLATFORM = (
    f"Unknown platform, expected one of {list(PATTERNS.keys())}"
)


class Extraction:
    """Extracted profiles."""

    _hrefs: list[str]

    def __init__(self, hrefs: list[str]) -> None:
        self._hrefs = hrefs

    def get_matches_per_platform(self) -> dict[str, list[str]]:
        """
        Get lists of profiles keyed by platform name.

        :return: a dictionary with the platform as a key,
            and a list of the platform's profiles as values.
        """
        return extract_matches_per_platform(self._hrefs)

    def get_matches_for_platform(self, platform: str) -> list[str]:
        """
        Find all matches for a specific platform.

        :param platform: platform to search for.
        :return: list of matches.
        """
        return extract_matches_for_platform(platform, self._hrefs)


def extract_matches_per_platform(hrefs: list[str]) -> dict[str, list[str]]:
    """
    Get lists of profiles keyed by platform name.

    :param hrefs: hrefs to parse.
    :return: a dictionary with the platform as a key,
        and a list of the platform's profiles as values.
    """
    matches: dict[str, list[str]] = {}
    for platform in PATTERNS:
        platform_matches = extract_matches_for_platform(platform, hrefs)
        matches[platform] = platform_matches
    return matches


def extract_matches_for_platform(platform: str, hrefs: list[str]) -> list[str]:
    matches: list[str] = []
    for href in hrefs:
        if platform == get_platform(href):
            result = _clean_href(href, platform)
            matches.append(result)
    return matches


def _clean_href(href: str, platform: str) -> str:
    """Cleans a href for a specific platform."""
    result = href
    cleaner = get_cleaner(platform)
    if cleaner:
        result = cleaner(href)
    return result


def get_platform(href: str) -> str | None:
    for platform in PATTERNS:
        is_match = is_platform(href, platform)
        if is_match:
            return platform
    return None


def is_platform(href: str, platform: str) -> bool:
    if platform not in PATTERNS:
        raise RuntimeError(ERROR_MSG_UNKNOWN_PLATFORM)
    return any(re.match(p, href) for p in PATTERNS[platform])


def clean_mailto(href: str) -> str:
    return href.replace("mailto:", "")


def get_cleaner(platform: str) -> Callable[[str], str] | None:
    cleaners: dict[str, Callable[[str], str]] = {
        PLATFORM_EMAIL: clean_mailto,
    }

    if platform not in cleaners:
        return None
    return cleaners[platform]
