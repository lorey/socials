# socials

Turn URLs into structured social media profiles.

You have a list of URLs from a scrape, a CSV export, or email signatures.
Some of them are social media profiles.
Socials finds them and gives you structured data to work with.

## Quick Start

```bash
pip install socials
```

```python
import socials

repo = socials.parse("https://github.com/lorey/socials")
print(repo)
# GitHubRepoURL(owner='lorey', repo='socials')

print(repo.platform)
# 'github'

print(repo.owner)
# 'lorey'
```

## Supported Platforms

| Platform   | Entity Types     | Example URL                          |
|------------|------------------|--------------------------------------|
| GitHub     | profile, repo    | github.com/lorey/socials             |
| Twitter/X  | profile          | twitter.com/karllorey                |
| LinkedIn   | profile, company | linkedin.com/in/karllorey            |
| Facebook   | profile          | facebook.com/zuck                    |
| Instagram  | profile          | instagram.com/instagram              |
| YouTube    | channel          | youtube.com/c/GoogleDevelopers       |
| Email      | email            | mailto:hello@example.com             |
| Phone      | phone            | tel:+1234567890                      |

## What You Get

Each URL is parsed into a typed Python object:

- `platform` - Which social network
- `entity_type` - Profile, repo, company, etc.
- Platform-specific fields like `username`, `repo`, `company_name`

No regex. No string parsing. Just data.

## Next Steps

- [Getting Started](getting-started.md) - Full tutorial with real-world examples
- [CLI Reference](cli.md) - Process URLs from the command line
- [API Reference](reference.md) - Full API documentation

### Architecture

- [Overview](architecture.md) - How socials works
- [Parsers](parsers.md) - Platform-specific URL parsers
- [Registry](registry.md) - URL routing
- [URLs](urls.md) - Typed URL objects
- [Extraction](extraction.md) - Extractor and results

## Related Projects

- [Socials API](https://github.com/lorey/socials-api) - REST API wrapper for socials
- [Social Media Profiles Regexs](https://github.com/lorey/social-media-profiles-regexs) - Regex collection for social media URL detection

## Links

- [Source Code](https://github.com/lorey/socials)
- [PyPI](https://pypi.org/project/socials/)
- [Changelog](changelog.md)
