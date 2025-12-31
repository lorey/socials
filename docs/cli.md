# CLI Reference

The `socials` CLI processes URLs from files or stdin.
Useful for batch processing, shell scripts, and pipeline integration.

After installing socials, the `socials` command is available in your terminal.

## Commands

### check

Identify what platform a URL belongs to:

```bash
socials check <url>
```

**Examples:**

```bash
$ socials check https://github.com/lorey
github

$ socials check https://twitter.com/karllorey
twitter

$ socials check https://example.com
unknown
```

Returns exit code 1 if the URL doesn't match any known platform.

### extract

Extract social profiles from URLs:

```bash
socials extract [file]
```

Reads URLs from a file (one per line) or from stdin if no file is provided.

**Examples:**

```bash
# From a file
$ socials extract urls.txt
facebook    https://facebook.com/peterparker
github      https://github.com/lorey

# From stdin
$ echo "https://github.com/lorey" | socials extract
github      https://github.com/lorey

# Filter by platform
$ socials extract urls.txt --platform github
https://github.com/lorey
```

**Options:**

- `-p, --platform`: Filter results to a specific platform

## Pipeline Examples

The CLI works well with other Unix tools:

```bash
# Filter for specific platforms with jq
cat urls.txt | socials extract | jq '.[] | select(.platform == "linkedin")'

# Count profiles by platform
cat urls.txt | socials extract | jq 'group_by(.platform) | map({platform: .[0].platform, count: length})'

# Extract just usernames
cat urls.txt | socials extract | jq -r '.[] | .username // .company_name // .email'

# Pre-filter URLs before processing
grep -h "linkedin\|twitter\|github" scraped_data.txt | socials extract

# Save results to a file
socials extract urls.txt > profiles.json
```

## Global Options

- `-v, --version`: Show version and exit
- `--help`: Show help message
