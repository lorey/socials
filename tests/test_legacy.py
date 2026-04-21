"""Tests for deprecated 0.x API to ensure backwards compatibility."""

import warnings

import pytest

import socials
from socials.extractor import Extraction


class TestLegacyExtractFunction:
    """Tests for the deprecated socials.extract() function."""

    def test_extract_emits_deprecation_warning(self):
        with pytest.warns(DeprecationWarning, match="extract.*deprecated"):
            socials.extract(["https://github.com/lorey"])

    def test_extract_returns_extraction(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            result = socials.extract(["https://github.com/lorey"])
        assert isinstance(result, Extraction)
        assert len(result.all()) == 1

    def test_extract_multiple_urls(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            result = socials.extract(
                [
                    "https://github.com/lorey",
                    "https://twitter.com/karllorey",
                ],
            )
        assert len(result.all()) == 2


class TestLegacyExtractionMethods:
    """Tests for deprecated Extraction methods."""

    def test_get_matches_per_platform_emits_warning(self):
        extraction = socials.parse_all(["https://github.com/lorey"])
        with pytest.warns(DeprecationWarning, match="get_matches_per_platform"):
            extraction.get_matches_per_platform()

    def test_get_matches_per_platform_returns_strings(self):
        extraction = socials.parse_all(["https://github.com/lorey"])
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            result = extraction.get_matches_per_platform()
        assert "github" in result
        assert isinstance(result["github"][0], str)

    def test_get_matches_for_platform_emits_warning(self):
        extraction = socials.parse_all(["https://github.com/lorey"])
        with pytest.warns(DeprecationWarning, match="get_matches_for_platform"):
            extraction.get_matches_for_platform("github")

    def test_get_matches_for_platform_returns_strings(self):
        extraction = socials.parse_all(["https://github.com/lorey"])
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            result = extraction.get_matches_for_platform("github")
        assert len(result) == 1
        assert isinstance(result[0], str)

    def test_get_matches_for_platform_empty(self):
        extraction = socials.parse_all(["https://github.com/lorey"])
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            result = extraction.get_matches_for_platform("twitter")
        assert result == []


class TestLegacyFullExtraction:
    """Comprehensive test for deprecated 0.x API behavior."""

    def test_extract_filters_invalid_and_groups_by_platform(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)

            urls = [
                "http://google.de",
                "http://facebook.com",
                "http://facebook.com/peterparker",
                "http://facebook.com/peter[parker",  # Invalid character
                "https://www.facebook.com/profile.php?id=4",
                "mailto:bill@microsoft.com",
                "steve@microsoft.com",
                "https://www.linkedin.com/company/google/",
                "https://www.linkedin.com/comp^any/google/",  # Invalid character
                "http://www.twitter.com/Some_Company/",
                "http://www.twitter.com/Some_\\Company",  # Invalid character
                "https://www.instagram.com/instagram/",
                "https://www.instagram.com/instag-ram/",  # Invalid character
                "http://instagr.am/instagram",
                "http://youtube.com/this/is/too/long",
                "http://www.youtube.com/user/Some_1",
                "http://youtube.com/c/your-custom-name",
                "http://youtube.com/your.custom.name",
            ]
            extraction = socials.extract(urls)
            matches = extraction.get_matches_per_platform()

            assert "facebook" in matches
            assert len(matches["facebook"]) == 2
            assert "http://facebook.com/peterparker" in matches["facebook"]
            assert "https://www.facebook.com/profile.php?id=4" in matches["facebook"]

            assert "email" in matches
            assert len(matches["email"]) == 2
            assert "bill@microsoft.com" in matches["email"]
            assert "steve@microsoft.com" in matches["email"]

            assert "linkedin" in matches
            assert len(matches["linkedin"]) == 1
            assert "https://www.linkedin.com/company/google/" in matches["linkedin"]

            assert "twitter" in matches
            assert len(matches["twitter"]) == 1
            assert "http://www.twitter.com/Some_Company/" in matches["twitter"]

            assert "instagram" in matches
            assert len(matches["instagram"]) == 2
            assert "https://www.instagram.com/instagram/" in matches["instagram"]
            assert "http://instagr.am/instagram" in matches["instagram"]

            assert "youtube" in matches
            assert len(matches["youtube"]) == 3
            assert "http://www.youtube.com/user/Some_1" in matches["youtube"]
            assert "http://youtube.com/c/your-custom-name" in matches["youtube"]
            assert "http://youtube.com/your.custom.name" in matches["youtube"]
