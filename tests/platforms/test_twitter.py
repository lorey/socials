"""Tests for Twitter/X platform parser."""

import pytest

from socials.platforms.twitter import TwitterParser, TwitterProfileURL


class TestTwitterParser:
    """Tests for TwitterParser."""

    @pytest.fixture
    def parser(self):
        return TwitterParser()

    # Hostname tests

    @pytest.mark.parametrize(
        "hostname",
        [
            "twitter.com",
            "www.twitter.com",
            "x.com",
            "www.x.com",
            "mobile.twitter.com",
            "mobile.x.com",
        ],
    )
    def test_handles_valid_hostname(self, parser, hostname):
        assert parser.handles_hostname(hostname) is True

    @pytest.mark.parametrize(
        "hostname",
        [
            "api.twitter.com",
            "twiter.com",
            "twitter.co",
        ],
    )
    def test_rejects_invalid_hostname(self, parser, hostname):
        assert parser.handles_hostname(hostname) is False

    # Profile URL tests

    @pytest.mark.parametrize(
        ("url", "username"),
        [
            ("https://twitter.com/karllorey", "karllorey"),
            ("https://twitter.com/karllorey/", "karllorey"),
            ("http://twitter.com/karllorey", "karllorey"),
            ("https://www.twitter.com/karllorey", "karllorey"),
            ("https://x.com/karllorey", "karllorey"),
            ("https://www.x.com/karllorey", "karllorey"),
            ("https://mobile.twitter.com/karllorey", "karllorey"),
            ("https://twitter.com/@karllorey", "karllorey"),
            ("https://twitter.com/Some_Company", "Some_Company"),
        ],
    )
    def test_parse_profile(self, parser, url, username):
        result = parser.parse(url)
        assert isinstance(result, TwitterProfileURL)
        assert result.url == url
        assert result.username == username
        assert result.platform == "twitter"
        assert result.entity_type == "profile"

    # Reserved path rejection

    @pytest.mark.parametrize(
        "url",
        [
            "https://twitter.com/home",
            "https://twitter.com/explore",
            "https://twitter.com/settings",
            "https://twitter.com/messages",
            "https://twitter.com/i",
            "https://twitter.com/login",
            "https://twitter.com/search",
            "https://twitter.com/compose",
            "https://x.com/home",
            "https://x.com/explore",
        ],
    )
    def test_rejects_reserved_paths(self, parser, url):
        assert parser.parse(url) is None

    # Invalid URLs

    @pytest.mark.parametrize(
        "url",
        [
            "https://twitter.com/user/status/123456",
            "https://twitter.com",
            "https://twitter.com/",
            "https://twitter.com/user/followers",
        ],
    )
    def test_rejects_invalid_urls(self, parser, url):
        assert parser.parse(url) is None


class TestTwitterProfileURL:
    """Tests for TwitterProfileURL."""

    @pytest.fixture
    def profile(self):
        return TwitterProfileURL(
            url="https://twitter.com/karllorey",
            username="karllorey",
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
            "url": "https://twitter.com/karllorey",
            "platform": "twitter",
            "entity_type": "profile",
            "username": "karllorey",
        }
