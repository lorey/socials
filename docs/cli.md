# CLI Reference

Socials provides a command-line interface for quick URL checking and extraction.

## Commands

### check

Check which platform a URL belongs to.

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

Extract social media URLs from input.

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

## Global Options

- `-v, --version`: Show version and exit
- `--help`: Show help message
