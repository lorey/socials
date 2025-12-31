"""Tests for Facebook platform parser."""

import pytest

from socials.platforms.facebook import FacebookParser, FacebookProfileURL


class TestFacebookParser:
    """Tests for FacebookParser."""

    @pytest.fixture
    def parser(self):
        return FacebookParser()

    # Hostname tests

    @pytest.mark.parametrize(
        "hostname",
        [
            "facebook.com",
            "www.facebook.com",
            "fb.com",
            "www.fb.com",
            "m.facebook.com",
        ],
    )
    def test_handles_valid_hostname(self, parser, hostname):
        assert parser.handles_hostname(hostname) is True

    @pytest.mark.parametrize(
        "hostname",
        [
            "facbook.com",
            "facebook.co",
            "facebookcom",
        ],
    )
    def test_rejects_invalid_hostname(self, parser, hostname):
        assert parser.handles_hostname(hostname) is False

    # Profile URL tests (by username)

    @pytest.mark.parametrize(
        ("url", "username"),
        [
            ("http://facebook.com/peterparker", "peterparker"),
            ("http://facebook.com/peterparker/", "peterparker"),
            ("https://facebook.com/peterparker", "peterparker"),
            ("https://www.facebook.com/peterparker", "peterparker"),
            ("https://fb.com/peterparker", "peterparker"),
            ("https://facebook.com/some.page", "some.page"),
            ("https://facebook.com/Some_Page", "Some_Page"),
        ],
    )
    def test_parse_profile_username(self, parser, url, username):
        result = parser.parse(url)
        assert isinstance(result, FacebookProfileURL)
        assert result.url == url
        assert result.username == username
        assert result.user_id is None
        assert result.platform == "facebook"
        assert result.entity_type == "profile"

    # Profile URL tests (by ID)

    @pytest.mark.parametrize(
        ("url", "user_id"),
        [
            ("https://www.facebook.com/profile.php?id=4", "4"),
            ("https://facebook.com/profile.php?id=123456789", "123456789"),
        ],
    )
    def test_parse_profile_id(self, parser, url, user_id):
        result = parser.parse(url)
        assert isinstance(result, FacebookProfileURL)
        assert result.url == url
        assert result.user_id == user_id
        assert result.username is None
        assert result.platform == "facebook"
        assert result.entity_type == "profile"

    # Reserved path rejection

    @pytest.mark.parametrize(
        "url",
        [
            "https://facebook.com/marketplace",
            "https://facebook.com/gaming",
            "https://facebook.com/watch",
            "https://facebook.com/groups",
            "https://facebook.com/messages",
            "https://facebook.com/help",
        ],
    )
    def test_rejects_reserved_paths(self, parser, url):
        assert parser.parse(url) is None

    # Invalid URLs

    @pytest.mark.parametrize(
        "url",
        [
            "https://facebook.com",
            "https://facebook.com/",
            "http://facebook.com/peter[parker",  # Invalid character
            "https://facebook.com/profile.php",  # Missing ID
        ],
    )
    def test_rejects_invalid_urls(self, parser, url):
        assert parser.parse(url) is None


class TestFacebookProfileURL:
    """Tests for FacebookProfileURL."""

    @pytest.fixture
    def profile_username(self):
        return FacebookProfileURL(
            url="https://facebook.com/peterparker",
            username="peterparker",
        )

    @pytest.fixture
    def profile_id(self):
        return FacebookProfileURL(
            url="https://facebook.com/profile.php?id=123",
            user_id="123",
        )

    def test_hierarchy_is_root(self, profile_username):
        assert profile_username.get_parent() is None
        assert profile_username.get_root() == profile_username
        assert profile_username.get_ancestors() == []

    def test_hashable(self, profile_username):
        assert hash(profile_username) == hash(profile_username.url)
        s = {profile_username}
        assert profile_username in s

    def test_model_dump_username(self, profile_username):
        d = profile_username.model_dump()
        assert d == {
            "url": "https://facebook.com/peterparker",
            "platform": "facebook",
            "entity_type": "profile",
            "username": "peterparker",
            "user_id": None,
        }

    def test_model_dump_id(self, profile_id):
        d = profile_id.model_dump()
        assert d == {
            "url": "https://facebook.com/profile.php?id=123",
            "platform": "facebook",
            "entity_type": "profile",
            "username": None,
            "user_id": "123",
        }
