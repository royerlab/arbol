# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Arbol is a Python package for arborescent (tree-like) console output. It organizes stdout prints in a visual hierarchy that matches code structure using context managers. The name means "tree" in Spanish.

## Commands

```sh
make install       # Install hatch and set up environment
make test          # Run all tests
make demo          # Run the demo
make lint          # Run linter (ruff)
make format        # Format code (ruff)
make check         # Run all checks (lint + format)
make build         # Build package
make clean         # Clean build artifacts
make publish       # Bump version, run checks & tests, commit, tag, and push
make publish-patch # Publish patch version (for same-day releases)
```

Or use hatch directly:
```sh
hatch run test     # Run tests
hatch run demo     # Run demo
hatch build        # Build package
hatch shell        # Enter environment shell
```

## Architecture

The entire library is in `arbol/arbol.py` (~285 lines). Key components:

- **`Arbol` class**: Configuration holder using class variables. Manages global state including `_depth` (current nesting level), output flags, colors, and Unicode box-drawing characters. Uses thread-local storage for capture state.

- **`aprint(*args, ...)`**: Drop-in replacement for built-in `print()`. Adds tree scaffolding based on current depth.

- **`asection(section_header)`**: Context manager that creates tree nodes. Increments depth on enter, decrements on exit, measures and displays elapsed time.

- **`section(section_header)`**: Function decorator wrapping `asection`.

- **`acapture()`**: Context manager to capture stdout/stderr from third-party code and redirect into the tree structure (experimental).

## Key Configuration (Arbol class attributes)

| Attribute | Default | Description |
|-----------|---------|-------------|
| `enable_output` | `True` | Set to `False` to suppress all output |
| `elapsed_time` | `True` | Set to `False` to hide timing information |
| `max_depth` | `math.inf` | Maximum tree depth (deeper sections show truncation) |
| `colorful` | `True` | Set to `False` to disable colors |
| `passthrough` | `False` | Set to `True` to bypass tree formatting entirely |

## Dependencies

Core library has zero hard dependencies. Optional extras:
- `pip install arbol[colors]` - Color support (ansicolors + colorama)
- `pip install arbol[dev]` - Development dependencies (pytest + colors)

## Publishing

Uses PyPI trusted publishers with GitHub Actions. The workflow (`.github/workflows/publish.yml`) triggers on version tags (`v*`). To publish:
```sh
make publish       # Updates version to today's date (e.g., 2025.2.1)
make publish-patch # For same-day releases (e.g., 2025.2.1.1)
```
