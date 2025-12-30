# API Reference

## Main Function

### socials.extract(urls)

Extract social media profiles from a list of URLs.

**Parameters:**

- `urls` (list[str]): List of URLs to analyze

**Returns:**

- `Extraction`: Object with methods to retrieve matches

**Example:**

```python
import socials

urls = ["https://github.com/lorey", "https://example.com"]
extraction = socials.extract(urls)
```

## Extraction Class

### get_matches_per_platform()

Get all matches grouped by platform name.

**Returns:**

- `dict[str, list[str]]`: Dictionary with platform names as keys and lists of matching URLs as values

**Example:**

```python
results = extraction.get_matches_per_platform()
# {
#     'facebook': ['https://facebook.com/user'],
#     'github': ['https://github.com/lorey'],
#     'twitter': [],
#     ...
# }
```

### get_matches_for_platform(platform)

Get matches for a specific platform.

**Parameters:**

- `platform` (str): Platform name (e.g., "github", "facebook")

**Returns:**

- `list[str]`: List of matching URLs

**Example:**

```python
github_urls = extraction.get_matches_for_platform("github")
# ['https://github.com/lorey']
```

## Platform Constants

Available platform identifiers:

- `socials.socials.PLATFORM_FACEBOOK` = "facebook"
- `socials.socials.PLATFORM_GITHUB` = "github"
- `socials.socials.PLATFORM_LINKEDIN` = "linkedin"
- `socials.socials.PLATFORM_TWITTER` = "twitter"
- `socials.socials.PLATFORM_INSTAGRAM` = "instagram"
- `socials.socials.PLATFORM_YOUTUBE` = "youtube"
- `socials.socials.PLATFORM_EMAIL` = "email"

## Utility Functions

### socials.socials.get_platform(href)

Detect which platform a URL belongs to.

**Parameters:**

- `href` (str): URL to check

**Returns:**

- `str | None`: Platform name or None if not recognized

### socials.socials.is_platform(href, platform)

Check if a URL belongs to a specific platform.

**Parameters:**

- `href` (str): URL to check
- `platform` (str): Platform name to check against

**Returns:**

- `bool`: True if the URL belongs to the platform

**Raises:**

- `RuntimeError`: If platform is not recognized
