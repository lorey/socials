# -*- coding: utf-8 -*-

"""Main module."""
import re

PLATFORM_FACEBOOK = 'facebook'
PLATFORM_GITHUB = 'github'
PLATFORM_LINKEDIN = 'linkedin'
PLATFORM_TWITTER = 'twitter'

FACEBOOK_URL_REGEXS = [
    'http(s)?://(www\.)?(facebook|fb)\.com/[A-z0-9_\-\.]+/?',
]

GITHUB_URL_REGEXS = [
    'http(s)?://(www\.)?github\.com/[A-z0-9_-]+/?',
]

LINKEDIN_URL_REGEXS = [
    # private
    'http(s)?://([\w]+\.)?linkedin\.com/in/(A-z0-9_-)+/?',
    'http(s)?://([\w]+\.)?linkedin\.com/pub/[A-z0-9_-]+(\/[A-z 0-9]+){3}/?',
    # companies
    'http(s)?://(www\.)?linkedin\.com/company/(A-z0-9_-)+/?',
]

TWITTER_URL_REGEXS = [
    'http(s)?://(.*\.)?twitter\.com\/[A-z0-9_]+/?',
]


PATTERNS = {
    PLATFORM_FACEBOOK: FACEBOOK_URL_REGEXS,
    PLATFORM_TWITTER: TWITTER_URL_REGEXS,
    PLATFORM_LINKEDIN: LINKEDIN_URL_REGEXS,
    PLATFORM_GITHUB: GITHUB_URL_REGEXS,
}


class Extraction(object):
    """Extracted profiles."""

    _urls = None

    def __init__(self, urls):
        self._urls = urls

    def get_matches_per_platform(self):
        """
        Get lists of profiles keyed by platform name.
        :return: a dictionary with the platform as a key,
        and a list of the platform's profiles as values
        """
        return extract_matches_per_platform(self._urls)


def extract_matches_per_platform(urls):
    """
    Get lists of profiles keyed by platform name.
    :return: a dictionary with the platform as a key,
    and a list of the platform's profiles as values
    """
    matches = {}
    for url in urls:
        platform = get_platform(url)
        if platform:
            if platform not in matches:
                matches[platform] = []
            matches[platform].append(url)
    return matches


def get_platform(url):
    for platform in PATTERNS:
        is_match = is_platform(url, platform)
        if is_match:
            return platform
    return None


def is_platform(url, platform):
    if platform not in PATTERNS:
        raise RuntimeError('Unknown platform, expected one of %s' % PATTERNS.keys())
    return any(re.match(p, url) for p in PATTERNS[platform])
