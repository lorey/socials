"""Miscellaneous URL types (email, phone)."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, ClassVar, Literal
from urllib.parse import unquote

from pydantic import BaseModel

if TYPE_CHECKING:
    from socials.protocols import SocialsURL


class EmailURL(BaseModel, frozen=True):
    """Email address (mailto: URL or plain email)."""

    url: str
    platform: Literal["email"] = "email"
    entity_type: Literal["email"] = "email"
    email: str

    def __hash__(self) -> int:
        """Return hash based on URL."""
        return hash(self.url)

    def get_parent(self) -> None:
        """Return parent (None for emails)."""
        return

    def get_root(self) -> EmailURL:
        """Return root of hierarchy (self for emails)."""
        return self

    def get_ancestors(self) -> list[SocialsURL]:
        """Return ancestors (empty for emails)."""
        return []


class PhoneURL(BaseModel, frozen=True):
    """Phone number (tel: URL)."""

    url: str
    platform: Literal["phone"] = "phone"
    entity_type: Literal["phone"] = "phone"
    number: str

    def __hash__(self) -> int:
        """Return hash based on URL."""
        return hash(self.url)

    def get_parent(self) -> None:
        """Return parent (None for phone numbers)."""
        return

    def get_root(self) -> PhoneURL:
        """Return root of hierarchy (self for phone numbers)."""
        return self

    def get_ancestors(self) -> list[SocialsURL]:
        """Return ancestors (empty for phone numbers)."""
        return []


class EmailParser:
    """Parser for email addresses."""

    platform = "email"
    schemes: ClassVar[set[str]] = {"mailto"}

    def handles_hostname(self, _hostname: str) -> bool:
        """Email doesn't use hostnames (routes by scheme instead)."""
        return False

    def parse(self, url: str) -> EmailURL | None:
        """Parse an email address or mailto: URL."""
        # Handle mailto: URLs
        if url.lower().startswith("mailto:"):
            email = unquote(url[7:].split("?")[0])  # Remove query params
        else:
            email = url

        # Basic email validation
        if not re.match(r"^[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}$", email):
            return None

        return EmailURL(
            url=url,
            email=email,
        )


class PhoneParser:
    """Parser for phone numbers."""

    platform = "phone"
    schemes: ClassVar[set[str]] = {"tel"}

    def handles_hostname(self, _hostname: str) -> bool:
        """Phone doesn't use hostnames (routes by scheme instead)."""
        return False

    def parse(self, url: str) -> PhoneURL | None:
        """Parse a tel: URL."""
        if not url.lower().startswith("tel:"):
            return None

        number = unquote(url[4:])

        # Basic phone validation (digits, spaces, dashes, parens, plus)
        if not re.match(r"^[+\d\s().-]+$", number):
            return None

        return PhoneURL(
            url=url,
            number=number,
        )
