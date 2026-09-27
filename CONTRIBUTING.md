# Contributing

## Principles

1. Keep skills platform-neutral when possible.
2. Keep model names and CLI-specific syntax inside `adapters/`.
3. Prefer deterministic verification over model self-review.
4. Cheap workers must escalate instead of guessing.
5. Installation must be additive and idempotent.

## Code rules

Enforced by `make rules` (`scripts/check_code_rules.py`) and ruff (`PLR0913`, `max-args = 5`):

| Rule | Limit | Scope |
|---|---|---|
| Lines per file | <= 300 | `*.py`, `*.sh`, `*.ps1` |
| Lines per function / method | <= 30 (signature, decorators and docstring included) | Python |
| Parameters per function | <= 5 (`self` / `cls` excluded; `*args` / `**kwargs` counted) | Python |

When a limit is hit, split the file or extract helpers / a parameter object. Do not add suppressions.

## Skill authoring

- `description` in `SKILL.md` frontmatter must state when to use the skill (`Use when ...`) and must be valid YAML — do not put `: ` in an unquoted value.
- Every bundled file (`scripts/`, `references/`, `templates/`) must be referenced from `SKILL.md`, with commands written relative to the skill directory.
- `make validate` enforces all of the above.

## Validation

```bash
make setup   # first time only
make check   # must pass before committing
```

Keep `VERSION` and `pyproject.toml` `version` in sync (enforced by `scripts/validate.py`).
