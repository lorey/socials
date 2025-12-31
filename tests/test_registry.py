"""Tests for Registry class."""

import warnings
from typing import ClassVar

import pytest

from socials.platforms.github import GitHubParser
from socials.platforms.misc import EmailParser, PhoneParser
from socials.registry import Registry


class TestRegistry:
    def test_init_empty(self):
        reg = Registry()
        assert reg.parsers == []

    def test_init_with_parsers(self):
        reg = Registry([GitHubParser()])
        assert len(reg.parsers) == 1

    def test_register_parser(self):
        reg = Registry()
        reg.register(GitHubParser())
        assert len(reg.parsers) == 1
        assert reg.parsers[0].platform == "github"

    def test_get_parser_for_hostname(self):
        reg = Registry([GitHubParser()])
        parser = reg.get_parser_for_hostname("github.com")
        assert parser is not None
        assert parser.platform == "github"

    def test_get_parser_for_hostname_www(self):
        reg = Registry([GitHubParser()])
        parser = reg.get_parser_for_hostname("www.github.com")
        assert parser is not None
        assert parser.platform == "github"

    def test_get_parser_for_unknown_hostname(self):
        reg = Registry([GitHubParser()])
        parser = reg.get_parser_for_hostname("gitlab.com")
        assert parser is None

    def test_get_parser_for_scheme_mailto(self):
        reg = Registry([EmailParser()])
        parser = reg.get_parser_for_scheme("mailto")
        assert parser is not None
        assert parser.platform == "email"

    def test_get_parser_for_scheme_tel(self):
        reg = Registry([PhoneParser()])
        parser = reg.get_parser_for_scheme("tel")
        assert parser is not None
        assert parser.platform == "phone"

    def test_get_parser_for_unknown_scheme(self):
        reg = Registry([GitHubParser()])
        parser = reg.get_parser_for_scheme("ftp")
        assert parser is None

    def test_get_parser_for_url_https(self):
        reg = Registry([GitHubParser()])
        parser = reg.get_parser_for_url("https://github.com/lorey")
        assert parser is not None
        assert parser.platform == "github"

    def test_get_parser_for_url_mailto(self):
        reg = Registry([EmailParser()])
        parser = reg.get_parser_for_url("mailto:test@example.com")
        assert parser is not None
        assert parser.platform == "email"

    def test_get_parser_for_url_tel(self):
        reg = Registry([PhoneParser()])
        parser = reg.get_parser_for_url("tel:+1234567890")
        assert parser is not None
        assert parser.platform == "phone"

    def test_get_parser_for_url_raw_email(self):
        """Raw emails without mailto: should still find the parser."""
        reg = Registry([EmailParser()])
        parser = reg.get_parser_for_url("test@example.com")
        assert parser is not None
        assert parser.platform == "email"

    def test_get_parser_for_url_unknown(self):
        reg = Registry([GitHubParser()])
        parser = reg.get_parser_for_url("https://gitlab.com/user")
        assert parser is None

    def test_parse_github_url(self):
        reg = Registry([GitHubParser()])
        result = reg.parse("https://github.com/lorey")
        assert result is not None
        assert result.platform == "github"
        assert result.username == "lorey"

    def test_parse_email_url(self):
        reg = Registry([EmailParser()])
        result = reg.parse("mailto:test@example.com")
        assert result is not None
        assert result.platform == "email"
        assert result.email == "test@example.com"

    def test_parse_returns_none_for_unknown(self):
        reg = Registry([GitHubParser()])
        result = reg.parse("https://gitlab.com/user")
        assert result is None

    def test_parse_returns_none_for_empty_registry(self):
        reg = Registry()
        result = reg.parse("https://github.com/lorey")
        assert result is None

    @pytest.mark.parametrize(
        ("url", "expected_platform"),
        [
            ("https://github.com/lorey", "github"),
            ("mailto:test@example.com", "email"),
            ("tel:+1234567890", "phone"),
            ("test@example.com", "email"),
        ],
    )
    def test_parse_multiple_parsers(self, url, expected_platform):
        reg = Registry([GitHubParser(), EmailParser(), PhoneParser()])
        result = reg.parse(url)
        assert result is not None
        assert result.platform == expected_platform


class TestRegistryOverlappingParsers:
    """Tests documenting the 'first match wins' behavior for overlapping parsers."""

    def test_first_registered_parser_wins_for_hostname(self):
        """First registered parser takes priority for same hostname."""

        class ParserA:
            platform = "parser_a"
            schemes: ClassVar[set[str]] = {"http", "https"}

            def handles_hostname(self, hostname: str) -> bool:
                return hostname == "example.com"

            def parse(self, _url: str) -> None:
                return None

        class ParserB:
            platform = "parser_b"
            schemes: ClassVar[set[str]] = {"http", "https"}

            def handles_hostname(self, hostname: str) -> bool:
                return hostname == "example.com"

            def parse(self, _url: str) -> None:
                return None

        reg = Registry()
        reg.register(ParserA())
        reg.register(ParserB())

        # First registered parser wins
        parser = reg.get_parser_for_hostname("example.com")
        assert parser is not None
        assert parser.platform == "parser_a"

    def test_no_warning_for_http_https_overlap(self):
        """No warning for http/https overlap since hostname routing handles it."""

        class ParserA:
            platform = "parser_a"
            schemes: ClassVar[set[str]] = {"http", "https"}

            def handles_hostname(self, hostname: str) -> bool:
                return hostname == "a.com"

            def parse(self, _url: str) -> None:
                return None

        class ParserB:
            platform = "parser_b"
            schemes: ClassVar[set[str]] = {"http", "https"}

            def handles_hostname(self, hostname: str) -> bool:
                return hostname == "b.com"

            def parse(self, _url: str) -> None:
                return None

        reg = Registry()
        # No warning expected for http/https overlap
        with warnings.catch_warnings():
            warnings.simplefilter("error")  # Turn warnings into errors
            reg.register(ParserA())
            reg.register(ParserB())

        assert len(reg.parsers) == 2

    def test_overlapping_non_http_schemes_warns(self):
        """Registering a parser with overlapping non-http schemes issues a warning."""

        class ParserA:
            platform = "parser_a"
            schemes: ClassVar[set[str]] = {"mailto"}

            def handles_hostname(self, _hostname: str) -> bool:
                return False

            def parse(self, _url: str) -> None:
                return None

        class ParserB:
            platform = "parser_b"
            schemes: ClassVar[set[str]] = {"mailto"}  # Overlaps with ParserA

            def handles_hostname(self, _hostname: str) -> bool:
                return False

            def parse(self, _url: str) -> None:
                return None

        reg = Registry()
        reg.register(ParserA())

        with pytest.warns(UserWarning, match="overlapping schemes"):
            reg.register(ParserB())

    def test_no_warning_for_distinct_schemes(self):
        """No warning when parsers have distinct schemes."""
        reg = Registry()

        # These have distinct schemes, no warning expected
        with warnings.catch_warnings():
            warnings.simplefilter("error")  # Turn warnings into errors
            reg.register(EmailParser())  # mailto
            reg.register(PhoneParser())  # tel
            reg.register(GitHubParser())  # http, https

        assert len(reg.parsers) == 3
