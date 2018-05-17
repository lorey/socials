# -*- coding: utf-8 -*-

"""Top-level package for Socials."""
from socials.socials import Extraction

__author__ = """Karl Lorey"""
__email__ = 'git@karllorey.com'
__version__ = '0.1.0'


def extract(urls):
    return Extraction(urls).get_matches_per_platform()
