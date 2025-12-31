"""GitHub platform parser and URL types."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, ClassVar, Literal

from pydantic import BaseModel

if TYPE_CHECKING:
    from socials.protocols import SocialsURL

# Reserved paths that are not usernames
_RESERVED = (
    "about|codespaces|collections|contact|customer-stories|enterprise|events|"
    "explore|features|issues|login|marketplace|new|notifications|orgs|pricing|"
    "pulls|readme|search|security|settings|sponsors|team|topics|trending"
)

# Regex patterns with named groups
# Adapted from: https://github.com/lorey/social-media-profiles-regexs
REPO_REGEX = re.compile(
    rf"^https?://(?:www\.)?github\.com/(?P<owner>(?!{_RESERVED})[A-Za-z0-9_-]+)/"
    r"(?P<repo>[A-Za-z0-9._-]+)/?$",
)
PROFILE_REGEX = re.compile(
    rf"^https?://(?:www\.)?github\.com/(?P<username>(?!{_RESERVED})[A-Za-z0-9_-]+)/?$",
)


class GitHubProfileURL(BaseModel, frozen=True):
    """GitHub user or organization profile URL."""

    url: str
    platform: Literal["github"] = "github"
    entity_type: Literal["profile"] = "profile"
    username: str

    def __hash__(self) -> int:
        """Return hash based on URL."""
        return hash(self.url)

    def get_parent(self) -> None:
        """Return parent (None for profiles)."""
        return

    def get_root(self) -> GitHubProfileURL:
        """Return root of hierarchy (self for profiles)."""
        return self

    def get_ancestors(self) -> list[SocialsURL]:
        """Return ancestors (empty for profiles)."""
        return []


class GitHubRepoURL(BaseModel, frozen=True):
    """GitHub repository URL."""

    url: str
    platform: Literal["github"] = "github"
    entity_type: Literal["repo"] = "repo"
    owner: str
    repo: str

    def __hash__(self) -> int:
        """Return hash based on URL."""
        return hash(self.url)

    def get_parent(self) -> GitHubProfileURL:
        """Return parent profile."""
        return GitHubProfileURL(
            url=f"https://github.com/{self.owner}",
            username=self.owner,
        )

    def get_root(self) -> GitHubProfileURL:
        """Return root of hierarchy."""
        return self.get_parent()

    def get_ancestors(self) -> list[SocialsURL]:
        """Return ancestors."""
        return [self.get_parent()]


class GitHubParser:
    """Parser for GitHub URLs."""

    platform = "github"
    schemes: ClassVar[set[str]] = {"http", "https"}

    def handles_hostname(self, hostname: str) -> bool:
        """Check if this parser handles the given hostname."""
        return hostname in {"github.com", "www.github.com"}

    def parse(self, url: str) -> GitHubProfileURL | GitHubRepoURL | None:
        """Parse a GitHub URL into a typed object."""
        # Try repo first (more specific)
        if match := REPO_REGEX.match(url):
            return GitHubRepoURL(url=url, **match.groupdict())

        # Try profile
        if match := PROFILE_REGEX.match(url):
            return GitHubProfileURL(url=url, **match.groupdict())

        return None
