"""Tests for LinkedIn platform parser."""

import pytest

from socials.platforms.linkedin import (
    LinkedInCompanyURL,
    LinkedInParser,
    LinkedInProfileURL,
)


class TestLinkedInParser:
    """Tests for LinkedInParser."""

    @pytest.fixture
    def parser(self):
        return LinkedInParser()

    # Hostname tests

    @pytest.mark.parametrize(
        "hostname",
        [
            "linkedin.com",
            "www.linkedin.com",
            "de.linkedin.com",
            "uk.linkedin.com",
            "fr.linkedin.com",
        ],
    )
    def test_handles_valid_hostname(self, parser, hostname):
        assert parser.handles_hostname(hostname) is True

    @pytest.mark.parametrize(
        "hostname",
        [
            "linkedn.com",
            "linkedin.co",
            "mylinkedin.com",
        ],
    )
    def test_rejects_invalid_hostname(self, parser, hostname):
        assert parser.handles_hostname(hostname) is False

    # Profile URL tests (/in/)

    @pytest.mark.parametrize(
        ("url", "username"),
        [
            ("https://linkedin.com/in/karllorey", "karllorey"),
            ("https://linkedin.com/in/karllorey/", "karllorey"),
            ("https://www.linkedin.com/in/karllorey", "karllorey"),
            ("https://de.linkedin.com/in/karllorey", "karllorey"),
            ("https://linkedin.com/in/karl-lorey", "karl-lorey"),
            ("https://linkedin.com/in/karl_lorey", "karl_lorey"),
            ("http://linkedin.com/in/karllorey", "karllorey"),
        ],
    )
    def test_parse_profile_in(self, parser, url, username):
        result = parser.parse(url)
        assert isinstance(result, LinkedInProfileURL)
        assert result.url == url
        assert result.username == username
        assert result.platform == "linkedin"
        assert result.entity_type == "profile"

    # Profile URL tests (/pub/)

    @pytest.mark.parametrize(
        ("url", "username"),
        [
            ("https://linkedin.com/pub/karl-lorey/1/2/3", "karl-lorey"),
            ("https://www.linkedin.com/pub/john-doe/a/b/c", "john-doe"),
        ],
    )
    def test_parse_profile_pub(self, parser, url, username):
        result = parser.parse(url)
        assert isinstance(result, LinkedInProfileURL)
        assert result.url == url
        assert result.username == username

    # Company URL tests

    @pytest.mark.parametrize(
        ("url", "company_id"),
        [
            ("https://linkedin.com/company/google", "google"),
            ("https://linkedin.com/company/google/", "google"),
            ("https://www.linkedin.com/company/google", "google"),
            ("https://linkedin.com/company/some-company", "some-company"),
            ("https://linkedin.com/school/mit", "mit"),
            ("https://linkedin.com/school/stanford-university", "stanford-university"),
        ],
    )
    def test_parse_company(self, parser, url, company_id):
        result = parser.parse(url)
        assert isinstance(result, LinkedInCompanyURL)
        assert result.url == url
        assert result.company_id == company_id
        assert result.platform == "linkedin"
        assert result.entity_type == "company"

    # Invalid URLs

    @pytest.mark.parametrize(
        "url",
        [
            "https://linkedin.com",
            "https://linkedin.com/",
            "https://linkedin.com/in/",
            "https://linkedin.com/company/",
            "https://linkedin.com/jobs/view/123",
            "https://linkedin.com/feed",
        ],
    )
    def test_rejects_invalid_urls(self, parser, url):
        assert parser.parse(url) is None


class TestLinkedInProfileURL:
    """Tests for LinkedInProfileURL."""

    @pytest.fixture
    def profile(self):
        return LinkedInProfileURL(
            url="https://linkedin.com/in/karllorey",
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


class TestLinkedInCompanyURL:
    """Tests for LinkedInCompanyURL."""

    @pytest.fixture
    def company(self):
        return LinkedInCompanyURL(
            url="https://linkedin.com/company/google",
            company_id="google",
        )

    def test_hierarchy_is_root(self, company):
        assert company.get_parent() is None
        assert company.get_root() == company
        assert company.get_ancestors() == []

    def test_hashable(self, company):
        assert hash(company) == hash(company.url)
        s = {company}
        assert company in s
