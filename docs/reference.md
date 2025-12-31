# API Reference

Auto-generated API documentation from source code.

## Module Functions

::: socials.parse
    options:
      show_root_heading: true
      heading_level: 3

::: socials.parse_all
    options:
      show_root_heading: true
      heading_level: 3

## Classes

::: socials.Extractor
    options:
      show_root_heading: true
      heading_level: 3
      members:
        - parse
        - extract

::: socials.Extraction
    options:
      show_root_heading: true
      heading_level: 3
      members:
        - all
        - by_platform
        - by_type

::: socials.registry.Registry
    options:
      show_root_heading: true
      heading_level: 3

## Protocols

::: socials.protocols.SocialsURL
    options:
      show_root_heading: true
      heading_level: 3

::: socials.protocols.PlatformParser
    options:
      show_root_heading: true
      heading_level: 3

::: socials.protocols.ParseError
    options:
      show_root_heading: true
      heading_level: 3

## Platform URL Types

All URL types implement the `SocialsURL` protocol (see above) with `get_parent()`, `get_root()`, and `get_ancestors()` methods. Below are the platform-specific attributes for each type.

### GitHub

::: socials.platforms.github.GitHubProfileURL
    options:
      show_root_heading: true
      heading_level: 4
      members: false

::: socials.platforms.github.GitHubRepoURL
    options:
      show_root_heading: true
      heading_level: 4
      members: false

### Twitter

::: socials.platforms.twitter.TwitterProfileURL
    options:
      show_root_heading: true
      heading_level: 4
      members: false

### LinkedIn

::: socials.platforms.linkedin.LinkedInProfileURL
    options:
      show_root_heading: true
      heading_level: 4
      members: false

::: socials.platforms.linkedin.LinkedInCompanyURL
    options:
      show_root_heading: true
      heading_level: 4
      members: false

### Facebook

::: socials.platforms.facebook.FacebookProfileURL
    options:
      show_root_heading: true
      heading_level: 4
      members: false

### Instagram

::: socials.platforms.instagram.InstagramProfileURL
    options:
      show_root_heading: true
      heading_level: 4
      members: false

### YouTube

::: socials.platforms.youtube.YouTubeChannelURL
    options:
      show_root_heading: true
      heading_level: 4
      members: false

### Email and Phone

::: socials.platforms.misc.EmailURL
    options:
      show_root_heading: true
      heading_level: 4
      members: false

::: socials.platforms.misc.PhoneURL
    options:
      show_root_heading: true
      heading_level: 4
      members: false
