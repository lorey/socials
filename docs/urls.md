# URL Objects

When you parse a URL with socials, you get back a typed URL object. These objects contain structured data extracted from the URL.

## The SocialsURL Protocol

All URL objects implement the `SocialsURL` protocol:

```
class SocialsURL(Protocol):
    url: str
    platform: str
    entity_type: str

    def get_parent(self) -> SocialsURL | None: ...
    def get_root(self) -> SocialsURL: ...
    def get_ancestors(self) -> list[SocialsURL]: ...
```

## Core Properties

Every URL object has these properties:

| Property | Type | Description |
|----------|------|-------------|
| `url` | `str` | The original URL string |
| `platform` | `str` | Platform identifier (`"github"`, `"twitter"`, etc.) |
| `entity_type` | `str` | Entity type (`"profile"`, `"repo"`, `"channel"`, etc.) |

## Platform-Specific Properties

Each URL type has additional properties for extracted data:

```python
import socials

# GitHub repo
repo = socials.parse("https://github.com/lorey/socials")
print(repo.owner)
# "lorey"

print(repo.repo)
# "socials"

# Twitter profile
profile = socials.parse("https://twitter.com/karllorey")
print(profile.username)
# "karllorey"

# YouTube channel
channel = socials.parse("https://youtube.com/channel/UC_x5XG1OV2P6uZZ5FSM9Ttw")
print(channel.channel_id)
# "UC_x5XG1OV2P6uZZ5FSM9Ttw"

# Email
email = socials.parse("mailto:hello@example.com")
print(email.email)
# "hello@example.com"
```

## Hierarchy Navigation

URL objects can have parent-child relationships. For example, a GitHub issue belongs to a repo, which belongs to a profile.

### Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `get_parent()` | `SocialsURL \| None` | Immediate parent |
| `get_root()` | `SocialsURL` | Top of hierarchy |
| `get_ancestors()` | `list[SocialsURL]` | Full chain from parent to root |

### Example

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

### Flat Platforms

Some platforms don't have hierarchy. For these, `get_parent()` returns `None` and `get_root()` returns `self`:

```python
import socials

profile = socials.parse("https://twitter.com/karllorey")
print(profile.get_parent())
# None

print(profile.get_root() == profile)
# True

print(profile.get_ancestors())
# []
```

## Immutability

All URL objects are immutable (Pydantic models with `frozen=True`). This means:

- They can be used as dictionary keys or in sets
- They're safe to share between threads
- You can't accidentally modify them

```python
import socials

repo = socials.parse("https://github.com/lorey/socials")

# Use as dict key
cache = {repo: "cached data"}

# Use in sets
urls = {repo, repo}
print(len(urls))
# 1
```

## Serialization

URL objects can be serialized to dictionaries or JSON:

```python
import socials
import json

repo = socials.parse("https://github.com/lorey/socials")

print(repo.model_dump())
# {"url": "...", "platform": "github", "entity_type": "repo", ...}

json.dumps(repo.model_dump())
```

## URL Types by Platform

| Platform | Entity Types | URL Class |
|----------|--------------|-----------|
| GitHub | profile | `GitHubProfileURL` |
| GitHub | repo | `GitHubRepoURL` |
| Twitter | profile | `TwitterProfileURL` |
| LinkedIn | profile | `LinkedInProfileURL` |
| LinkedIn | company | `LinkedInCompanyURL` |
| Facebook | profile | `FacebookProfileURL` |
| Instagram | profile | `InstagramProfileURL` |
| YouTube | channel | `YouTubeChannelURL` |
| Email | email | `EmailURL` |
| Phone | phone | `PhoneURL` |
