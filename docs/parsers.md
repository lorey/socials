# Parsers

Parsers are responsible for recognizing and extracting data from URLs of a specific platform.

## The PlatformParser Protocol

Every parser implements the `PlatformParser` protocol:

```
class PlatformParser(Protocol):
    platform: str
    schemes: ClassVar[set[str]]

    def handles_hostname(self, hostname: str) -> bool: ...
    def parse(self, url: str) -> SocialsURL | None: ...
```

### Attributes

- **`platform`**: String identifier (e.g., `"github"`, `"twitter"`)
- **`schemes`**: Set of URL schemes the parser handles (e.g., `{"http", "https"}` or `{"mailto"}`)

### Methods

- **`handles_hostname(hostname)`**: Returns `True` if the parser can handle URLs from this hostname
- **`parse(url)`**: Parses the URL and returns a typed URL object, or `None` if not recognized

## Built-in Parsers

| Parser | Platform | Hostnames | Entity Types |
|--------|----------|-----------|--------------|
| `GitHubParser` | github | github.com | profile, repo |
| `TwitterParser` | twitter | twitter.com, x.com | profile |
| `LinkedInParser` | linkedin | linkedin.com | profile, company |
| `FacebookParser` | facebook | facebook.com, fb.com | profile |
| `InstagramParser` | instagram | instagram.com | profile |
| `YouTubeParser` | youtube | youtube.com, youtu.be | channel |
| `EmailParser` | email | (mailto: scheme) | email |
| `PhoneParser` | phone | (tel: scheme) | phone |

## How Parsing Works

1. The [Registry](registry.md) receives a URL
2. It extracts the scheme (http, https, mailto, etc.)
3. For http/https URLs, it extracts the hostname and finds the matching parser via `handles_hostname()`
4. For other schemes (mailto, tel), it finds the parser that declares that scheme
5. The matched parser's `parse()` method is called
6. The parser returns a typed [URL object](urls.md) or `None`

## URL Evolution

URLs change over time. Parsers handle this gracefully:

- **Domain changes** (twitter.com to x.com): The parser's `handles_hostname()` accepts multiple hostnames
- **Path changes**: The parser handles multiple regex patterns, returning the same typed class

Example of handling multiple domains:

```
class TwitterParser:
    platform = "twitter"

    def handles_hostname(self, hostname: str) -> bool:
        return hostname in {"twitter.com", "x.com", "www.twitter.com", "www.x.com"}
```

## Parser Example

Here's a simplified view of how `GitHubParser` works:

```
REPO_REGEX = re.compile(
    r"^https?://(?:www\.)?github\.com/(?P<owner>[A-Za-z0-9_-]+)/"
    r"(?P<repo>[A-Za-z0-9._-]+)/?$"
)
PROFILE_REGEX = re.compile(
    r"^https?://(?:www\.)?github\.com/(?P<username>[A-Za-z0-9_-]+)/?$"
)

class GitHubParser:
    platform = "github"
    schemes: ClassVar[set[str]] = {"http", "https"}

    def handles_hostname(self, hostname: str) -> bool:
        return hostname in {"github.com", "www.github.com"}

    def parse(self, url: str) -> GitHubProfileURL | GitHubRepoURL | None:
        if match := REPO_REGEX.match(url):
            return GitHubRepoURL(url=url, **match.groupdict())
        if match := PROFILE_REGEX.match(url):
            return GitHubProfileURL(url=url, **match.groupdict())
        return None
```

Key points:
- More specific patterns are tried first (repo before profile)
- Named capture groups in regex map directly to URL object fields
- Returns `None` if the URL doesn't match any pattern

## Creating Custom Parsers

See [Contributing](contributing.md) for how to add a new platform parser.
