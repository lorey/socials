# Getting Started

This guide shows you how to use socials to parse and extract social media URLs.

## Installation

```bash
pip install socials
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv add socials
```

## Parsing a Single URL

Use `socials.parse()` to parse a single URL into a typed object:

```python
import socials

url = socials.parse("https://github.com/lorey/socials")

print(url.url)
# "https://github.com/lorey/socials"

print(url.platform)
# "github"

print(url.entity_type)
# "repo"

print(url.owner)
# "lorey"

print(url.repo)
# "socials"
```

If the URL isn't recognized, `parse()` returns `None`:

```python
import socials

result = socials.parse("https://example.com")
print(result)
# None
```

## Parsing Multiple URLs

Use `socials.parse_all()` to process a list of URLs:

```python
import socials

urls = [
    "https://github.com/lorey",
    "https://twitter.com/karllorey",
    "mailto:hello@example.com",
    "https://example.com",  # Not recognized, will be skipped
]

extraction = socials.parse_all(urls)

print(extraction.all())
# [GitHubProfileURL(...), TwitterProfileURL(...), EmailURL(...)]

print(extraction.by_platform())
# {"github": [...], "twitter": [...], "email": [...]}

print(extraction.by_type())
# {"profile": [...], "email": [...]}
```

## Working with Typed URL Objects

Each parsed URL is a typed object with structured data:

```python
import socials

# GitHub
github = socials.parse("https://github.com/lorey/socials")
print(github.owner)
# "lorey"

print(github.repo)
# "socials"

# Twitter
twitter = socials.parse("https://twitter.com/karllorey")
print(twitter.username)
# "karllorey"

# LinkedIn
linkedin = socials.parse("https://linkedin.com/company/google")
print(linkedin.entity_type)
# "company"

print(linkedin.company_id)
# "google"

# Email
email = socials.parse("mailto:hello@example.com")
print(email.email)
# "hello@example.com"
```

## Navigating Hierarchies

Some URLs have parent-child relationships. For example, a GitHub repo belongs to a profile:

```python
import socials

repo = socials.parse("https://github.com/lorey/socials")

profile = repo.get_parent()
print(profile.url)
# "https://github.com/lorey"

print(profile.username)
# "lorey"

root = repo.get_root()
print(root == profile)
# True

print(repo.get_ancestors())
# [GitHubProfileURL(...)]
```

For flat platforms (no hierarchy), `get_parent()` returns `None`:

```python
import socials

twitter = socials.parse("https://twitter.com/karllorey")
print(twitter.get_parent())
# None
```

## Filtering by Platform

Only parse URLs from specific platforms:

```python
from socials import Extractor

extractor = Extractor(platforms=["github", "twitter"])

result = extractor.parse("https://linkedin.com/in/karllorey")
print(result)
# None (LinkedIn not in list)

result = extractor.parse("https://github.com/lorey")
print(result)
# GitHubProfileURL(...)
```

## Strict Mode

By default, unrecognized URLs return `None`. Use strict mode to raise errors instead:

```python
from socials import Extractor
from socials.protocols import ParseError

extractor = Extractor(strict=True)

try:
    extractor.parse("https://example.com")
except ParseError as e:
    print(f"Failed to parse: {e}")
```

## Serialization

URL objects can be serialized to dictionaries:

```python
import socials

repo = socials.parse("https://github.com/lorey/socials")

print(repo.model_dump())
# {
#     "url": "https://github.com/lorey/socials",
#     "platform": "github",
#     "entity_type": "repo",
#     "owner": "lorey",
#     "repo": "socials"
# }
```

## Real-World Examples

### Extracting Profiles from a Scraped Website

You've scraped a company's "About" page and have a list of hrefs:

```python
import socials

urls = [
    "https://acme.com/about",
    "https://linkedin.com/company/acme",
    "https://twitter.com/acme",
    "https://github.com/acme",
    "/contact",
]

result = socials.parse_all(urls)
for profile in result.all():
    print(f"{profile.platform}: {profile.url}")
# linkedin: https://linkedin.com/company/acme
# twitter: https://twitter.com/acme
# github: https://github.com/acme
```

### Finding Social Links in Email Data

Processing email signatures or footers:

```python
import socials

urls = [
    "https://linkedin.com/company/acme-corp",
    "https://twitter.com/acme",
]

result = socials.parse_all(urls)
linkedin = result.by_platform().get("linkedin", [])

if linkedin:
    print(f"Found company: {linkedin[0].company_id}")
# Found company: acme-corp
```

### Batch Processing with the CLI

Process a file of URLs:

```bash
socials extract urls.txt > profiles.json
```

Pipe from another command:

```bash
grep -h "linkedin\|twitter\|github" scraped_data.txt | socials extract
```

Integrate into a shell pipeline:

```bash
cat urls.txt | socials extract | jq '.[] | select(.platform == "github")'
```

## Supported Platforms

| Platform | Example URL |
|----------|-------------|
| GitHub | `https://github.com/lorey` |
| Twitter/X | `https://twitter.com/karllorey` |
| LinkedIn | `https://linkedin.com/in/karllorey` |
| Facebook | `https://facebook.com/zuck` |
| Instagram | `https://instagram.com/instagram` |
| YouTube | `https://youtube.com/c/GoogleDevelopers` |
| Email | `mailto:hello@example.com` |
| Phone | `tel:+1234567890` |

## Next Steps

- [CLI Reference](cli.md) - Use socials from the command line
- [Architecture](architecture.md) - Understand how socials works
- [API Reference](reference.md) - Full API documentation
