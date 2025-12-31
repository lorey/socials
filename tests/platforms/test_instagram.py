"""Tests for Instagram platform parser."""

import pytest

from socials.platforms.instagram import InstagramParser, InstagramProfileURL


class TestInstagramParser:
    """Tests for InstagramParser."""

    @pytest.fixture
    def parser(self):
        return InstagramParser()

    # Hostname tests

    @pytest.mark.parametrize(
        "hostname",
        [
            "instagram.com",
            "www.instagram.com",
            "instagr.am",
            "www.instagr.am",
        ],
    )
    def test_handles_valid_hostname(self, parser, hostname):
        assert parser.handles_hostname(hostname) is True

    @pytest.mark.parametrize(
        "hostname",
        [
            "instagam.com",
            "instagram.co",
            "m.instagram.com",
        ],
    )
    def test_rejects_invalid_hostname(self, parser, hostname):
        assert parser.handles_hostname(hostname) is False

    # Profile URL tests

    @pytest.mark.parametrize(
        ("url", "username"),
        [
            ("https://instagram.com/instagram", "instagram"),
            ("https://instagram.com/instagram/", "instagram"),
            ("https://www.instagram.com/instagram", "instagram"),
            ("http://instagram.com/instagram", "instagram"),
            ("http://instagr.am/instagram", "instagram"),
            ("https://instagram.com/some_user", "some_user"),
            ("https://instagram.com/user.name", "user.name"),
        ],
    )
    def test_parse_profile(self, parser, url, username):
        result = parser.parse(url)
        assert isinstance(result, InstagramProfileURL)
        assert result.url == url
        assert result.username == username
        assert result.platform == "instagram"
        assert result.entity_type == "profile"

    # Reserved path rejection

    @pytest.mark.parametrize(
        "url",
        [
            "https://instagram.com/about",
            "https://instagram.com/explore",
            "https://instagram.com/reels",
            "https://instagram.com/stories",
            "https://instagram.com/p",
            "https://instagram.com/tv",
            "https://instagram.com/direct",
            "https://instagram.com/accounts",
        ],
    )
    def test_rejects_reserved_paths(self, parser, url):
        assert parser.parse(url) is None

    # Invalid URLs

    @pytest.mark.parametrize(
        "url",
        [
            "https://instagram.com",
            "https://instagram.com/",
            "https://instagram.com/instag-ram",  # Invalid character (dash)
            "https://instagram.com/p/ABC123",  # Post URL
        ],
    )
    def test_rejects_invalid_urls(self, parser, url):
        assert parser.parse(url) is None


class TestInstagramProfileURL:
    """Tests for InstagramProfileURL."""

    @pytest.fixture
    def profile(self):
        return InstagramProfileURL(
            url="https://instagram.com/instagram",
            username="instagram",
        )

    def test_hierarchy_is_root(self, profile):
        assert profile.get_parent() is None
        assert profile.get_root() == profile
        assert profile.get_ancestors() == []

    def test_hashable(self, profile):
        assert hash(profile) == hash(profile.url)
        s = {profile}
        assert profile in s

    def test_model_dump(self, profile):
        d = profile.model_dump()
        assert d == {
            "url": "https://instagram.com/instagram",
            "platform": "instagram",
            "entity_type": "profile",
            "username": "instagram",
        }
