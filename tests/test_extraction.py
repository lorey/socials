"""Tests for Extraction result class."""

import warnings

import pytest

from socials.extractor import Extraction
from socials.platforms.github import GitHubProfileURL, GitHubRepoURL
from socials.platforms.twitter import TwitterProfileURL


class TestExtraction:
    @pytest.fixture
    def sample_results(self):
        return [
            GitHubProfileURL(url="https://github.com/lorey", username="lorey"),
            GitHubRepoURL(
                url="https://github.com/lorey/socials",
                owner="lorey",
                repo="socials",
            ),
            TwitterProfileURL(
                url="https://twitter.com/karllorey",
                username="karllorey",
            ),
        ]

    def test_all_returns_all(self, sample_results):
        ext = Extraction(sample_results)
        assert len(ext.all()) == 3

    def test_all_returns_copy(self, sample_results):
        ext = Extraction(sample_results)
        result = ext.all()
        result.append(
            GitHubProfileURL(url="https://github.com/other", username="other"),
        )
        # Original should be unchanged
        assert len(ext.all()) == 3

    def test_by_platform(self, sample_results):
        ext = Extraction(sample_results)
        by_plat = ext.by_platform()
        assert len(by_plat["github"]) == 2
        assert len(by_plat["twitter"]) == 1

    def test_by_platform_returns_typed_objects(self, sample_results):
        ext = Extraction(sample_results)
        by_plat = ext.by_platform()
        # Should return typed objects, not strings
        assert isinstance(by_plat["github"][0], (GitHubProfileURL, GitHubRepoURL))
        assert isinstance(by_plat["twitter"][0], TwitterProfileURL)

    def test_by_type(self, sample_results):
        ext = Extraction(sample_results)
        by_type = ext.by_type()
        assert len(by_type["profile"]) == 2  # github profile + twitter profile
        assert len(by_type["repo"]) == 1

    def test_by_type_returns_typed_objects(self, sample_results):
        ext = Extraction(sample_results)
        by_type = ext.by_type()
        for item in by_type["profile"]:
            assert hasattr(item, "platform")
            assert hasattr(item, "entity_type")

    def test_empty_extraction(self):
        ext = Extraction([])
        assert ext.all() == []
        assert ext.by_platform() == {}
        assert ext.by_type() == {}

    # Backwards compat tests

    def test_get_matches_per_platform_deprecated(self, sample_results):
        ext = Extraction(sample_results)
        with pytest.warns(DeprecationWarning, match="get_matches_per_platform"):
            matches = ext.get_matches_per_platform()
        assert "github" in matches
        assert "twitter" in matches

    def test_get_matches_per_platform_returns_strings(self, sample_results):
        ext = Extraction(sample_results)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            matches = ext.get_matches_per_platform()
        # Should return strings, not objects
        assert isinstance(matches["github"][0], str)
        assert isinstance(matches["twitter"][0], str)

    def test_get_matches_for_platform_deprecated(self, sample_results):
        ext = Extraction(sample_results)
        with pytest.warns(DeprecationWarning, match="get_matches_for_platform"):
            matches = ext.get_matches_for_platform("twitter")
        assert len(matches) == 1

    def test_get_matches_for_platform_returns_strings(self, sample_results):
        ext = Extraction(sample_results)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            matches = ext.get_matches_for_platform("github")
        # Should return strings, not objects
        assert all(isinstance(m, str) for m in matches)
        assert "https://github.com/lorey" in matches
        assert "https://github.com/lorey/socials" in matches

    def test_get_matches_for_platform_empty(self, sample_results):
        ext = Extraction(sample_results)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            matches = ext.get_matches_for_platform("linkedin")
        assert matches == []
