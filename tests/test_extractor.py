"""Tests for Extractor class."""

import pytest

from socials.extractor import Extractor
from socials.platforms.github import GitHubProfileURL
from socials.protocols import ParseError


class TestExtractor:
    def test_parse_returns_typed_url(self):
        ext = Extractor()
        result = ext.parse("https://github.com/lorey")
        assert result is not None
        assert result.platform == "github"
        assert isinstance(result, GitHubProfileURL)

    def test_parse_returns_none_for_unknown(self):
        ext = Extractor()
        result = ext.parse("https://unknown.com/page")
        assert result is None

    def test_strict_mode_raises_parse_error(self):
        ext = Extractor(strict=True)
        with pytest.raises(ParseError, match="Unrecognized URL"):
            ext.parse("https://unknown.com/page")

    def test_strict_mode_returns_valid(self):
        ext = Extractor(strict=True)
        result = ext.parse("https://github.com/lorey")
        assert result is not None
        assert result.platform == "github"

    def test_extract_returns_extraction(self):
        ext = Extractor()
        result = ext.extract(["https://github.com/lorey"])
        assert len(result.all()) == 1

    def test_extract_filters_unrecognized(self):
        ext = Extractor()
        result = ext.extract(
            [
                "https://github.com/lorey",
                "https://unknown.com/page",
            ],
        )
        assert len(result.all()) == 1
        assert result.all()[0].platform == "github"

    def test_extract_multiple_platforms(self):
        ext = Extractor()
        result = ext.extract(
            [
                "https://github.com/lorey",
                "https://twitter.com/karllorey",
                "mailto:test@example.com",
            ],
        )
        assert len(result.all()) == 3
        platforms = {r.platform for r in result.all()}
        assert platforms == {"github", "twitter", "email"}

    def test_platforms_filter_include(self):
        ext = Extractor(platforms=["github"])
        # Should parse GitHub
        assert ext.parse("https://github.com/lorey") is not None
        # Should not parse Twitter (not in platforms list)
        assert ext.parse("https://twitter.com/lorey") is None

    def test_platforms_filter_multiple(self):
        ext = Extractor(platforms=["github", "twitter"])
        assert ext.parse("https://github.com/lorey") is not None
        assert ext.parse("https://twitter.com/lorey") is not None
        assert ext.parse("https://linkedin.com/in/lorey") is None

    def test_unknown_platform_raises_value_error(self):
        with pytest.raises(ValueError, match="Unknown platform"):
            Extractor(platforms=["nonexistent"])

    def test_empty_platforms_list(self):
        ext = Extractor(platforms=[])
        # Should not parse anything
        assert ext.parse("https://github.com/lorey") is None
        assert ext.parse("https://twitter.com/lorey") is None

    def test_extract_strict_mode_raises_on_first_unknown(self):
        ext = Extractor(strict=True)
        with pytest.raises(ParseError):
            ext.extract(
                [
                    "https://github.com/lorey",
                    "https://unknown.com/page",
                ],
            )

    def test_default_includes_all_platforms(self):
        ext = Extractor()
        # Test a few platforms to verify they're all included
        assert ext.parse("https://github.com/lorey") is not None
        assert ext.parse("https://twitter.com/lorey") is not None
        assert ext.parse("https://linkedin.com/in/lorey") is not None
        assert ext.parse("https://facebook.com/lorey") is not None
        assert ext.parse("https://instagram.com/lorey") is not None
        assert ext.parse("https://youtube.com/@lorey") is not None
        assert ext.parse("mailto:test@example.com") is not None
        assert ext.parse("tel:+1234567890") is not None
