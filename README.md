# Hyprland Wiki

Welcome to the Hyprland Wiki! Here we store the wiki pages. They are automatically updated on the
website whenever a change occurs, within a reasonable timeframe (usually 1–2 minutes).

You can find the site at [https://wiki.hypr.land/](https://wiki.hypr.land/)

## Quick Start

### Development Setup

1. **Install required tools:**
   - [Go](https://go.dev/doc/install) 1.22+
   - [Hugo Extended](https://gohugo.io/installation/) (latest)
   - Python 3.7+ (for validation scripts)

2. **Verify your environment:**
   ```bash
   python3 scripts/validate_env.py
   ```

3. **Start local development:**
   ```bash
   make serve
   # or: hugo serve
   ```

4. **View your changes:**
   Open [http://localhost:1313](http://localhost:1313)

### Making Changes

1. **Validate before committing:**
   ```bash
   make validate
   ```

2. **Follow commit conventions:**
   ```
   Dir/Page: summary of changes
   ```

3. **See full guidelines:**
   Read [CONTRIBUTING.md](./CONTRIBUTING.md) for detailed instructions

## Documentation

- **[CONTRIBUTING.md](./CONTRIBUTING.md)** - Complete contribution guide with examples
- **[ARCHITECTURE.md](./ARCHITECTURE.md)** - System design and defensive patterns
- **[scripts/README.md](./scripts/README.md)** - Validation tooling documentation

## Quality Assurance

This repository includes Python-based validation tools:

- **Configuration validation** - Checks Hugo config for defensive patterns
- **Content validation** - Ensures markdown quality and accessibility
- **Environment validation** - Verifies development setup

Run all checks:
```bash
make validate
```

## Contributing to the Wiki

Feel free to open an issue or a PR if you feel anything is necessary.
Make sure to clearly state the reason for the changes.

### Commit Format

Commits should have the form:

`Dir/Page: summary of changes`

Optionally, you can include a longer commit message 2 lines below the commit
title.

This format makes it easier to glance over the commit list and figure out what
each commit is about.

Additionally, if you make many changes in your PR, it is best to squash them
into self-contained commits that contain one logical change.

For info about how to squash commits, see [this](https://stackoverflow.com/a/5189600).

## Available Commands

Using the Makefile for convenience:

```bash
make help              # Show all available commands
make serve             # Start Hugo development server
make validate          # Run all validation checks
make validate-config   # Check configuration only
make validate-content  # Check markdown content only
make validate-env      # Check development environment
make build             # Build site with validation
make clean             # Remove generated files
```

## Local Development

To see your local changes, make sure to have `go` and `hugo` installed. Then, run

```sh
$ hugo serve
```

and open `http://localhost:1313` to see the locally-rendered wiki.

## Architecture

This wiki implements defensive design patterns for:
- **Robustness** - Graceful handling of edge cases
- **Accessibility** - WCAG compliance and screen reader support  
- **Maintainability** - Clear structure and validation tooling
- **Performance** - Fast builds and optimized output

See [ARCHITECTURE.md](./ARCHITECTURE.md) for detailed system design.

## License

This repository is licensed under the [BSD 3-Clause License](./LICENSE).
