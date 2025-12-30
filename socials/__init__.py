"""Top-level package for Socials."""

from importlib.metadata import version

from socials.socials import Extraction

__version__ = version("socials")


def extract(urls):
    return Extraction(urls)
