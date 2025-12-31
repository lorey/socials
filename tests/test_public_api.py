"""Tests for public API (module-level functions and exports)."""

import socials
from socials.extractor import Extraction, Extractor
from socials.platforms.github import GitHubProfileURL
from socials.protocols import ParseError, PlatformParser, SocialsURL


class TestModuleLevelFunctions:
    def test_parse_function(self):
        result = socials.parse("https://github.com/lorey")
        assert result is not None
        assert result.platform == "github"
        assert isinstance(result, GitHubProfileURL)

    def test_parse_returns_none_for_unknown(self):
        result = socials.parse("https://unknown.com/page")
        assert result is None

    def test_extract_function(self):
        result = socials.extract(["https://github.com/lorey"])
        assert isinstance(result, Extraction)
        assert len(result.all()) == 1

    def test_extract_multiple_urls(self):
        result = socials.extract(
            [
                "https://github.com/lorey",
                "https://twitter.com/karllorey",
            ],
        )
        assert len(result.all()) == 2


class TestExports:
    def test_version_exists(self):
        assert hasattr(socials, "__version__")
        assert isinstance(socials.__version__, str)

    def test_extractor_class_exported(self):
        assert hasattr(socials, "Extractor")
        assert socials.Extractor is Extractor

    def test_extraction_class_exported(self):
        assert hasattr(socials, "Extraction")
        assert socials.Extraction is Extraction

    def test_parse_error_exported(self):
        assert hasattr(socials, "ParseError")
        assert socials.ParseError is ParseError

    def test_socials_url_protocol_exported(self):
        assert hasattr(socials, "SocialsURL")
        assert socials.SocialsURL is SocialsURL

    def test_platform_parser_protocol_exported(self):
        assert hasattr(socials, "PlatformParser")
        assert socials.PlatformParser is PlatformParser

    def test_all_contains_expected_exports(self):
        expected = [
            "Extraction",
            "Extractor",
            "ParseError",
            "PlatformParser",
            "SocialsURL",
            "__version__",
            "extract",
            "parse",
        ]
        for name in expected:
            assert name in socials.__all__, f"{name} not in __all__"


class TestIntegration:
    def test_full_workflow(self):
        """Test a typical usage pattern."""
        urls = [
            "https://github.com/lorey/socials",
            "https://twitter.com/karllorey",
            "mailto:test@example.com",
            "https://unknown.com/page",  # Should be filtered
        ]

        extraction = socials.extract(urls)

        # Should have 3 valid results
        assert len(extraction.all()) == 3

        # Group by platform
        by_platform = extraction.by_platform()
        assert "github" in by_platform
        assert "twitter" in by_platform
        assert "email" in by_platform

        # Group by type
        by_type = extraction.by_type()
        assert "repo" in by_type
        assert "profile" in by_type
        assert "email" in by_type

    def test_hierarchy_traversal(self):
        """Test hierarchy methods work through the public API."""
        result = socials.parse("https://github.com/lorey/socials")
        assert result is not None

        # This is a repo, should have a parent profile
        parent = result.get_parent()
        assert parent is not None
        assert parent.platform == "github"
        assert parent.entity_type == "profile"

        # Root should also be the profile
        root = result.get_root()
        assert root.platform == "github"
        assert root.entity_type == "profile"

        # Ancestors should include the profile
        ancestors = result.get_ancestors()
        assert len(ancestors) == 1
        assert ancestors[0].entity_type == "profile"

    def test_custom_extractor(self):
        """Test creating a custom extractor with limited platforms."""
        ext = socials.Extractor(platforms=["github", "twitter"])

        # Should work for included platforms
        assert ext.parse("https://github.com/lorey") is not None
        assert ext.parse("https://twitter.com/karllorey") is not None

        # Should not work for excluded platforms
        assert ext.parse("mailto:test@example.com") is None
        assert ext.parse("https://linkedin.com/in/lorey") is None
