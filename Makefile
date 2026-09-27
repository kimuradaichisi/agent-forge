SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := help

UV     ?= uv
PYTHON ?= $(UV) run python
RUFF   ?= $(UV) run ruff
PY_SRC := scripts skills tests
SH_SRC := $(shell git ls-files '*.sh')
SKILLS := $(notdir $(wildcard skills/*))
CLAUDE_AGENTS := $(notdir $(wildcard adapters/claude/agents/*.md))

.PHONY: help setup clean-zone lint lint-py lint-sh rules format format-check test validate check ci map package clean skills-link skills-unlink

help: ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'

setup: ## Create .venv and install dev tools via uv
	$(UV) sync

clean-zone: ## Delete Windows *:Zone.Identifier files (WSL copy artifacts)
	@found=$$(find . -path ./.git -prune -o -path ./.venv -prune -o -type f -name '*Zone.Identifier' -print); \
	if [[ -n "$$found" ]]; then \
		echo "$$found" | sed 's/^/  removing /'; \
		find . -path ./.git -prune -o -path ./.venv -prune -o -type f -name '*Zone.Identifier' -exec rm -f {} +; \
	else \
		echo "clean-zone: no Zone.Identifier files"; \
	fi

lint: lint-py lint-sh ## Run all linters

lint-py: ## Lint Python with ruff
	$(RUFF) check $(PY_SRC)

lint-sh: ## Lint shell scripts with shellcheck
	$(UV) run shellcheck $(SH_SRC)

rules: ## Enforce code rules (file<=300 lines, function<=30 lines, params<=5)
	$(PYTHON) scripts/check_code_rules.py

format: ## Auto-format and auto-fix Python with ruff
	$(RUFF) format $(PY_SRC)
	$(RUFF) check --fix $(PY_SRC)

format-check: ## Verify formatting without modifying files
	$(RUFF) format --check $(PY_SRC)

test: ## Run unit tests (stdlib unittest)
	$(PYTHON) -m unittest discover -s tests

validate: ## Run repository structure / installer smoke validation
	$(PYTHON) scripts/validate.py

check: clean-zone lint format-check rules test validate ## Quality gate (Zone.Identifier cleanup, lint, format, rules, test, validate)

ci: lint format-check rules test validate ## Quality gate for CI (read-only)

map: ## Print the codebase symbol map
	@$(PYTHON) skills/codebase-cartographer/scripts/generate_map.py .

package: check ## Build dist/agent-forge-<VERSION>.zip
	$(PYTHON) scripts/package.py

skills-link: ## Dogfood: symlink skills/agents into .claude/ and .agents/ of this repo
	@link() { \
		if [[ -e "$$2" && ! -L "$$2" ]]; then echo "skills-link: $$2 exists and is not a symlink; remove it first" >&2; exit 1; fi; \
		mkdir -p "$$(dirname "$$2")"; ln -sfn "$$1" "$$2"; echo "  $$2 -> $$1"; \
	}; \
	for s in $(SKILLS); do \
		link "../../skills/$$s" ".claude/skills/$$s"; \
		link "../../skills/$$s" ".agents/skills/$$s"; \
	done; \
	for a in $(CLAUDE_AGENTS); do link "../../adapters/claude/agents/$$a" ".claude/agents/$$a"; done

skills-unlink: ## Remove symlinks created by skills-link
	@for s in $(SKILLS); do \
		for d in .claude/skills .agents/skills; do [[ -L "$$d/$$s" ]] && rm "$$d/$$s" && echo "  removed $$d/$$s"; done; \
	done; \
	for a in $(CLAUDE_AGENTS); do [[ -L ".claude/agents/$$a" ]] && rm ".claude/agents/$$a" && echo "  removed .claude/agents/$$a"; done; true

clean: clean-zone ## Remove caches and build output
	rm -rf dist .ruff_cache
	find . -path ./.git -prune -o -path ./.venv -prune -o -type d -name __pycache__ -exec rm -rf {} +
