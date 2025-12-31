"""Tests for Email and Phone parsers."""

import pytest

from socials.platforms.misc import EmailParser, EmailURL, PhoneParser, PhoneURL


class TestEmailParser:
    """Tests for EmailParser."""

    @pytest.fixture
    def parser(self):
        return EmailParser()

    def test_handles_hostname_always_false(self, parser):
        # Email routes by scheme, not hostname
        assert parser.handles_hostname("gmail.com") is False
        assert parser.handles_hostname("email.com") is False

    # Valid email tests

    @pytest.mark.parametrize(
        ("url", "email"),
        [
            ("mailto:test@example.com", "test@example.com"),
            ("mailto:bill@microsoft.com", "bill@microsoft.com"),
            ("MAILTO:TEST@EXAMPLE.COM", "TEST@EXAMPLE.COM"),
            ("mailto:user+tag@example.com", "user+tag@example.com"),
            ("mailto:test@example.com?subject=Hello", "test@example.com"),
            # Plain emails (without mailto:)
            ("test@example.com", "test@example.com"),
            ("bill@microsoft.com", "bill@microsoft.com"),
            ("user.name@example.co.uk", "user.name@example.co.uk"),
        ],
    )
    def test_parse_email(self, parser, url, email):
        result = parser.parse(url)
        assert isinstance(result, EmailURL)
        assert result.url == url
        assert result.email == email
        assert result.platform == "email"
        assert result.entity_type == "email"

    # Invalid email tests

    @pytest.mark.parametrize(
        "url",
        [
            "not-an-email",
            "mailto:",
            "mailto:invalid",
            "@example.com",
            "test@",
            "test@.com",
        ],
    )
    def test_rejects_invalid_emails(self, parser, url):
        assert parser.parse(url) is None


class TestEmailURL:
    """Tests for EmailURL."""

    @pytest.fixture
    def email_url(self):
        return EmailURL(
            url="mailto:test@example.com",
            email="test@example.com",
        )

    def test_hierarchy_is_root(self, email_url):
        assert email_url.get_parent() is None
        assert email_url.get_root() == email_url
        assert email_url.get_ancestors() == []

    def test_hashable(self, email_url):
        assert hash(email_url) == hash(email_url.url)
        s = {email_url}
        assert email_url in s

    def test_model_dump(self, email_url):
        d = email_url.model_dump()
        assert d == {
            "url": "mailto:test@example.com",
            "platform": "email",
            "entity_type": "email",
            "email": "test@example.com",
        }


class TestPhoneParser:
    """Tests for PhoneParser."""

    @pytest.fixture
    def parser(self):
        return PhoneParser()

    def test_handles_hostname_always_false(self, parser):
        # Phone routes by scheme, not hostname
        assert parser.handles_hostname("phone.com") is False

    # Valid phone tests

    @pytest.mark.parametrize(
        ("url", "number"),
        [
            ("tel:+1234567890", "+1234567890"),
            ("tel:+1 234 567 890", "+1 234 567 890"),
            ("tel:+1 (234) 567-890", "+1 (234) 567-890"),
            ("tel:123-456-7890", "123-456-7890"),
            ("TEL:+49123456789", "+49123456789"),
        ],
    )
    def test_parse_phone(self, parser, url, number):
        result = parser.parse(url)
        assert isinstance(result, PhoneURL)
        assert result.url == url
        assert result.number == number
        assert result.platform == "phone"
        assert result.entity_type == "phone"

    # Invalid phone tests

    @pytest.mark.parametrize(
        "url",
        [
            "tel:",
            "tel:abc",
            "tel:+1234abc",
            "+1234567890",  # Missing tel: prefix
            "phone:123456",
        ],
    )
    def test_rejects_invalid_phones(self, parser, url):
        assert parser.parse(url) is None


class TestPhoneURL:
    """Tests for PhoneURL."""

    @pytest.fixture
    def phone_url(self):
        return PhoneURL(
            url="tel:+1234567890",
            number="+1234567890",
        )

    def test_hierarchy_is_root(self, phone_url):
        assert phone_url.get_parent() is None
        assert phone_url.get_root() == phone_url
        assert phone_url.get_ancestors() == []

    def test_hashable(self, phone_url):
        assert hash(phone_url) == hash(phone_url.url)
        s = {phone_url}
        assert phone_url in s
