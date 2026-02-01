.PHONY: help install test demo lint format check build clean publish publish-patch

# Default target
help:
	@echo "Available commands:"
	@echo "  make install       - Install hatch and set up environment"
	@echo "  make test          - Run all tests"
	@echo "  make demo          - Run the demo"
	@echo "  make lint          - Run linter (ruff)"
	@echo "  make format        - Format code (ruff)"
	@echo "  make check         - Run all checks (lint + format check)"
	@echo "  make build         - Build package"
	@echo "  make clean         - Clean build artifacts"
	@echo "  make publish       - Bump version to today's date, commit, tag, and push"
	@echo "  make publish-patch - Publish patch version (for same-day releases)"

# =============================================================================
# Setup & Development
# =============================================================================

install:
	pip install hatch
	hatch env create

test:
	hatch run test

demo:
	hatch run demo

# =============================================================================
# Code Quality
# =============================================================================

lint:
	hatch run lint

format:
	hatch run format

check:
	@echo "Running linter..."
	@hatch run lint
	@echo "Checking formatting..."
	@hatch run format-check
	@echo "All checks passed!"

# =============================================================================
# Building
# =============================================================================

build: clean
	hatch build

clean:
	hatch clean 2>/dev/null || true
	rm -rf dist/ build/ *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

# =============================================================================
# Publishing
# =============================================================================

# Get current version from __init__.py
CURRENT_VERSION := $(shell grep -o "__version__ = '[^']*'" arbol/__init__.py | cut -d"'" -f2)
TODAY := $(shell date +%Y.%-m.%-d)

# Bump version to today's date and publish
publish: check test
	@echo "Current version: $(CURRENT_VERSION)"
	@if echo "$(CURRENT_VERSION)" | grep -q "^$(TODAY)"; then \
		echo "Error: Version $(CURRENT_VERSION) is already today's date."; \
		echo "Use 'make publish-patch' for same-day releases."; \
		exit 1; \
	fi
	@echo "Updating version to: $(TODAY)"
	@sed -i.bak "s/__version__ = '[^']*'/__version__ = '$(TODAY)'/" arbol/__init__.py && rm -f arbol/__init__.py.bak
	@echo "Committing version bump..."
	git add arbol/__init__.py
	git commit -m "$(TODAY) release."
	@echo "Creating tag v$(TODAY)..."
	git tag "v$(TODAY)"
	@echo "Pushing to origin..."
	git push origin main --tags
	@echo "Done! GitHub Actions will publish to PyPI."

# Publish patch version (for same-day releases)
publish-patch: check test
	@echo "Current version: $(CURRENT_VERSION)"
	@if echo "$(CURRENT_VERSION)" | grep -q "^$(TODAY)\."; then \
		PATCH=$$(echo "$(CURRENT_VERSION)" | sed 's/$(TODAY)\.\([0-9]*\)/\1/'); \
		NEW_PATCH=$$((PATCH + 1)); \
		NEW_VERSION="$(TODAY).$$NEW_PATCH"; \
	elif [ "$(CURRENT_VERSION)" = "$(TODAY)" ]; then \
		NEW_VERSION="$(TODAY).1"; \
	else \
		NEW_VERSION="$(TODAY)"; \
	fi; \
	echo "Updating version to: $$NEW_VERSION"; \
	sed -i.bak "s/__version__ = '[^']*'/__version__ = '$$NEW_VERSION'/" arbol/__init__.py && rm -f arbol/__init__.py.bak; \
	echo "Committing version bump..."; \
	git add arbol/__init__.py; \
	git commit -m "$$NEW_VERSION release."; \
	echo "Creating tag v$$NEW_VERSION..."; \
	git tag "v$$NEW_VERSION"; \
	echo "Pushing to origin..."; \
	git push origin main --tags; \
	echo "Done! GitHub Actions will publish to PyPI."
