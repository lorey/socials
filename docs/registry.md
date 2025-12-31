# Registry

The Registry is a dispatcher that routes URLs to the appropriate [parser](parsers.md).

## How It Works

```
URL → Registry → Parser → SocialsURL
```

1. **Extract scheme**: Is it `http`, `https`, `mailto`, `tel`, or something else?
2. **Route to parser**:
   - For http/https: Extract hostname, find parser via `handles_hostname()`
   - For other schemes: Find parser that declares that scheme
   - For no scheme (e.g., raw email): Try all parsers until one succeeds
3. **Parse**: Delegate to the matched parser's `parse()` method

## First-Match-Wins Policy

When multiple parsers could handle the same URL, the first registered parser takes priority. This prevents ambiguity and makes behavior predictable.

```python
from socials.registry import Registry
from socials.platforms.github import GitHubParser
from socials.platforms.twitter import TwitterParser

registry = Registry()
registry.register(GitHubParser())
registry.register(TwitterParser())
```

If you register a parser with overlapping schemes (other than http/https), you'll get a warning:

```
UserWarning: Parser 'new_email' has overlapping schemes {'mailto'}
with existing parser 'email'. First registered parser ('email') takes priority.
```

## Usage

The Registry is typically used internally by the [Extractor](extraction.md), but you can use it directly:

```python
from socials.registry import Registry
from socials.platforms.github import GitHubParser
from socials.platforms.twitter import TwitterParser

registry = Registry([GitHubParser(), TwitterParser()])

result = registry.parse("https://github.com/lorey/socials")
print(result)
# GitHubRepoURL(...)

parser = registry.get_parser_for_url("https://github.com/lorey")
print(parser.platform)
# "github"

parser = registry.get_parser_for_hostname("twitter.com")
print(parser.platform)
# "twitter"
```

## Registry Methods

| Method | Description |
|--------|-------------|
| `register(parser)` | Add a parser to the registry |
| `parse(url)` | Parse URL using appropriate parser |
| `get_parser_for_url(url)` | Find parser that handles a URL |
| `get_parser_for_hostname(hostname)` | Find parser for a hostname |
| `get_parser_for_scheme(scheme)` | Find parser for a URL scheme |
| `parsers` | Property returning list of registered parsers |

## When to Use Registry Directly

Most users should use the higher-level [Extractor](extraction.md) API. Use Registry directly when you need:

- Fine-grained control over parser registration order
- Custom routing logic
- To inspect which parser handles a URL without parsing it
