"""Tests for YouTube platform parser."""

import pytest

from socials.platforms.youtube import YouTubeChannelURL, YouTubeParser


class TestYouTubeParser:
    """Tests for YouTubeParser."""

    @pytest.fixture
    def parser(self):
        return YouTubeParser()

    # Hostname tests

    @pytest.mark.parametrize(
        "hostname",
        [
            "youtube.com",
            "www.youtube.com",
            "m.youtube.com",
        ],
    )
    def test_handles_valid_hostname(self, parser, hostname):
        assert parser.handles_hostname(hostname) is True

    @pytest.mark.parametrize(
        "hostname",
        [
            "youtu.be",
            "youtub.com",
            "youtube.co",
        ],
    )
    def test_rejects_invalid_hostname(self, parser, hostname):
        assert parser.handles_hostname(hostname) is False

    # Channel ID URL tests

    @pytest.mark.parametrize(
        ("url", "channel_id"),
        [
            (
                "https://youtube.com/channel/UCddiUEpeqJcYeBxX1IVBKvQ",
                "UCddiUEpeqJcYeBxX1IVBKvQ",
            ),
            (
                "https://www.youtube.com/channel/UCddiUEpeqJcYeBxX1IVBKvQ",
                "UCddiUEpeqJcYeBxX1IVBKvQ",
            ),
            (
                "http://youtube.com/channel/UCddiUEpeqJcYeBxX1IVBKvQ/",
                "UCddiUEpeqJcYeBxX1IVBKvQ",
            ),
        ],
    )
    def test_parse_channel_id(self, parser, url, channel_id):
        result = parser.parse(url)
        assert isinstance(result, YouTubeChannelURL)
        assert result.url == url
        assert result.channel_id == channel_id
        assert result.username is None
        assert result.custom_url is None
        assert result.platform == "youtube"
        assert result.entity_type == "channel"

    # User URL tests

    @pytest.mark.parametrize(
        ("url", "username"),
        [
            ("http://www.youtube.com/user/Some_1", "Some_1"),
            ("https://youtube.com/user/someuser", "someuser"),
            ("https://youtube.com/user/user.name", "user.name"),
        ],
    )
    def test_parse_user(self, parser, url, username):
        result = parser.parse(url)
        assert isinstance(result, YouTubeChannelURL)
        assert result.url == url
        assert result.username == username
        assert result.channel_id is None
        assert result.custom_url is None

    # Custom URL tests (/c/)

    @pytest.mark.parametrize(
        ("url", "custom_url"),
        [
            ("http://youtube.com/c/your-custom-name", "your-custom-name"),
            ("https://www.youtube.com/c/CustomChannel", "CustomChannel"),
        ],
    )
    def test_parse_custom_c(self, parser, url, custom_url):
        result = parser.parse(url)
        assert isinstance(result, YouTubeChannelURL)
        assert result.url == url
        assert result.custom_url == custom_url
        assert result.channel_id is None
        assert result.username is None

    # Handle URL tests (@)

    @pytest.mark.parametrize(
        ("url", "custom_url"),
        [
            ("https://youtube.com/@handle", "handle"),
            ("https://www.youtube.com/@SomeChannel", "SomeChannel"),
            ("https://youtube.com/@channel.name", "channel.name"),
        ],
    )
    def test_parse_handle(self, parser, url, custom_url):
        result = parser.parse(url)
        assert isinstance(result, YouTubeChannelURL)
        assert result.url == url
        assert result.custom_url == custom_url

    # Direct URL tests (just /channelname)

    @pytest.mark.parametrize(
        ("url", "custom_url"),
        [
            ("http://youtube.com/your.custom.name", "your.custom.name"),
            ("https://youtube.com/somechannel", "somechannel"),
        ],
    )
    def test_parse_direct(self, parser, url, custom_url):
        result = parser.parse(url)
        assert isinstance(result, YouTubeChannelURL)
        assert result.url == url
        assert result.custom_url == custom_url

    # Reserved path rejection

    @pytest.mark.parametrize(
        "url",
        [
            "https://youtube.com/watch",
            "https://youtube.com/shorts",
            "https://youtube.com/feed",
            "https://youtube.com/playlist",
            "https://youtube.com/trending",
            "https://youtube.com/gaming",
            "https://youtube.com/music",
            "https://youtube.com/premium",
        ],
    )
    def test_rejects_reserved_paths(self, parser, url):
        assert parser.parse(url) is None

    # Invalid URLs

    @pytest.mark.parametrize(
        "url",
        [
            "https://youtube.com",
            "https://youtube.com/",
            "https://youtube.com/watch?v=ABC123",
            "http://youtube.com/this/is/too/long",
            "https://youtu.be/ABC123",  # Different hostname
        ],
    )
    def test_rejects_invalid_urls(self, parser, url):
        assert parser.parse(url) is None


class TestYouTubeChannelURL:
    """Tests for YouTubeChannelURL."""

    @pytest.fixture
    def channel_id(self):
        return YouTubeChannelURL(
            url="https://youtube.com/channel/UCddiUEpeqJcYeBxX1IVBKvQ",
            channel_id="UCddiUEpeqJcYeBxX1IVBKvQ",
        )

    @pytest.fixture
    def channel_handle(self):
        return YouTubeChannelURL(
            url="https://youtube.com/@handle",
            custom_url="handle",
        )

    def test_hierarchy_is_root(self, channel_id):
        assert channel_id.get_parent() is None
        assert channel_id.get_root() == channel_id
        assert channel_id.get_ancestors() == []

    def test_hashable(self, channel_id):
        assert hash(channel_id) == hash(channel_id.url)
        s = {channel_id}
        assert channel_id in s

    def test_model_dump_channel_id(self, channel_id):
        d = channel_id.model_dump()
        assert d == {
            "url": "https://youtube.com/channel/UCddiUEpeqJcYeBxX1IVBKvQ",
            "platform": "youtube",
            "entity_type": "channel",
            "channel_id": "UCddiUEpeqJcYeBxX1IVBKvQ",
            "username": None,
            "custom_url": None,
        }

    def test_model_dump_handle(self, channel_handle):
        d = channel_handle.model_dump()
        assert d == {
            "url": "https://youtube.com/@handle",
            "platform": "youtube",
            "entity_type": "channel",
            "channel_id": None,
            "username": None,
            "custom_url": "handle",
        }
