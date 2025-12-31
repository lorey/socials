"""Base utilities for platform parsers."""

from __future__ import annotations

from urllib.parse import urlparse


def extract_hostname(url: str) -> str:
    """Extract hostname from URL.

    Args:
        url: Full URL string.

    Returns:
        Hostname (e.g., 'github.com' from 'https://github.com/user/repo').

    """
    parsed = urlparse(url)
    return parsed.netloc.lower()


def extract_scheme(url: str) -> str:
    """Extract scheme from URL.

    Args:
        url: Full URL string.

    Returns:
        Scheme (e.g., 'https', 'mailto', 'tel').

    """
    parsed = urlparse(url)
    return parsed.scheme.lower()


def extract_path_segments(url: str) -> list[str]:
    """Extract path segments from URL.

    Args:
        url: Full URL string.

    Returns:
        List of path segments, excluding empty strings.
        E.g., '/user/repo/' -> ['user', 'repo']

    """
    parsed = urlparse(url)
    path = parsed.path
    return [segment for segment in path.split("/") if segment]
