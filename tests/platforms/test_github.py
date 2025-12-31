"""Tests for GitHub platform parser."""

import pytest

from socials.platforms.github import GitHubParser, GitHubProfileURL, GitHubRepoURL


class TestGitHubParser:
    """Tests for GitHubParser."""

    @pytest.fixture
    def parser(self):
        return GitHubParser()

    # Hostname tests

    @pytest.mark.parametrize(
        "hostname",
        [
            "github.com",
            "www.github.com",
        ],
    )
    def test_handles_valid_hostname(self, parser, hostname):
        assert parser.handles_hostname(hostname) is True

    @pytest.mark.parametrize(
        "hostname",
        [
            "gist.github.com",
            "raw.githubusercontent.com",
            "gitlab.com",
            "bitbucket.org",
        ],
    )
    def test_rejects_invalid_hostname(self, parser, hostname):
        assert parser.handles_hostname(hostname) is False

    # Profile URL tests

    @pytest.mark.parametrize(
        ("url", "username"),
        [
            ("https://github.com/lorey", "lorey"),
            ("https://github.com/lorey/", "lorey"),
            ("http://github.com/lorey", "lorey"),
            ("https://www.github.com/lorey", "lorey"),
            ("https://github.com/some-org", "some-org"),
            ("https://github.com/user_name", "user_name"),
        ],
    )
    def test_parse_profile(self, parser, url, username):
        result = parser.parse(url)
        assert isinstance(result, GitHubProfileURL)
        assert result.url == url
        assert result.username == username
        assert result.platform == "github"
        assert result.entity_type == "profile"

    # Repo URL tests

    @pytest.mark.parametrize(
        ("url", "owner", "repo"),
        [
            ("https://github.com/lorey/socials", "lorey", "socials"),
            ("https://github.com/lorey/socials/", "lorey", "socials"),
            ("http://github.com/lorey/socials", "lorey", "socials"),
            ("https://www.github.com/lorey/socials", "lorey", "socials"),
            ("https://github.com/some-org/my-repo", "some-org", "my-repo"),
            ("https://github.com/user/repo.js", "user", "repo.js"),
            ("https://github.com/user/repo_name", "user", "repo_name"),
        ],
    )
    def test_parse_repo(self, parser, url, owner, repo):
        result = parser.parse(url)
        assert isinstance(result, GitHubRepoURL)
        assert result.url == url
        assert result.owner == owner
        assert result.repo == repo
        assert result.platform == "github"
        assert result.entity_type == "repo"

    # Reserved path rejection

    @pytest.mark.parametrize(
        "url",
        [
            "https://github.com/explore",
            "https://github.com/settings",
            "https://github.com/marketplace",
            "https://github.com/trending",
            "https://github.com/login",
            "https://github.com/pricing",
            "https://github.com/features",
        ],
    )
    def test_rejects_reserved_paths(self, parser, url):
        assert parser.parse(url) is None

    # Invalid URLs

    @pytest.mark.parametrize(
        "url",
        [
            "https://gitlab.com/user",
            "https://github.com/user/repo/issues",
            "https://github.com/user/repo/pull/123",
            "https://github.com",
            "https://github.com/",
        ],
    )
    def test_rejects_invalid_urls(self, parser, url):
        assert parser.parse(url) is None


class TestGitHubProfileURL:
    """Tests for GitHubProfileURL."""

    @pytest.fixture
    def profile(self):
        return GitHubProfileURL(url="https://github.com/lorey", username="lorey")

    def test_hierarchy_is_root(self, profile):
        assert profile.get_parent() is None
        assert profile.get_root() == profile
        assert profile.get_ancestors() == []

    def test_hashable(self, profile):
        assert hash(profile) == hash(profile.url)
        # Can be used in sets
        s = {profile}
        assert profile in s

    def test_model_dump(self, profile):
        d = profile.model_dump()
        assert d == {
            "url": "https://github.com/lorey",
            "platform": "github",
            "entity_type": "profile",
            "username": "lorey",
        }


class TestGitHubRepoURL:
    """Tests for GitHubRepoURL."""

    @pytest.fixture
    def repo(self):
        return GitHubRepoURL(
            url="https://github.com/lorey/socials",
            owner="lorey",
            repo="socials",
        )

    def test_get_parent_returns_profile(self, repo):
        parent = repo.get_parent()
        assert isinstance(parent, GitHubProfileURL)
        assert parent.username == "lorey"
        assert parent.url == "https://github.com/lorey"

    def test_get_root_returns_profile(self, repo):
        root = repo.get_root()
        assert isinstance(root, GitHubProfileURL)
        assert root.username == "lorey"

    def test_get_ancestors(self, repo):
        ancestors = repo.get_ancestors()
        assert len(ancestors) == 1
        assert isinstance(ancestors[0], GitHubProfileURL)

    def test_hashable(self, repo):
        assert hash(repo) == hash(repo.url)
        s = {repo}
        assert repo in s

    def test_model_dump(self, repo):
        d = repo.model_dump()
        assert d == {
            "url": "https://github.com/lorey/socials",
            "platform": "github",
            "entity_type": "repo",
            "owner": "lorey",
            "repo": "socials",
        }
