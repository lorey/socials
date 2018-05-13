# -*- coding: utf-8 -*-

"""Top-level package for Socials."""
import re

__author__ = """Karl Lorey"""
__email__ = 'git@karllorey.com'
__version__ = '0.1.0'

PATTERNS = {
    'facebook': [
        'http(s)?://(www\.)?(facebook|fb)\.com/[A-z0-9_\-\.]+/?'
    ],
    'twitter': [
        'http(s)?://(.*\.)?twitter\.com\/[A-z0-9_]+/?'
    ],
    'linkedin': [
        'http(s)?://([\w]+\.)?linkedin\.com/in/(A-z0-9_-)\/?',
        'http(s)?://([\w]+\.)?linkedin\.com/pub/[A-z0-9_-]+(\/[A-z 0-9]+){3}/?'
    ],
}


def extract(urls: list):
    matches = {}
    for url in urls:
        for plattform in PATTERNS:
            is_match = any(re.match(p, url) for p in PATTERNS[plattform])
            if is_match:
                if plattform not in matches:
                    matches[plattform] = []
                matches[plattform].append(url)

    return matches
