#!/usr/bin/env python3
import json
import re
import subprocess
import tempfile
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "README.md",
    "LICENSE",
    "VERSION",
    "pyproject.toml",
    "registry/skills.json",
    "registry/platforms.json",
    "skills/lean-routing/SKILL.md",
    "skills/scientific-debugging/SKILL.md",
    "skills/spec-driven-dev/SKILL.md",
    "skills/pr-guardian/SKILL.md",
    "skills/codebase-cartographer/SKILL.md",
    "installers/install.sh",
    "installers/uninstall.sh",
    "installers/install.ps1",
    "installers/uninstall.ps1",
    "adapters/claude/CLAUDE.md.snippet",
    "adapters/codex/AGENTS.md.snippet",
    "adapters/gemini/GEMINI.md.snippet",
]


SKILLS = ("lean-routing", "scientific-debugging", "spec-driven-dev", "pr-guardian", "codebase-cartographer")
SNIPPETS = {"claude": "CLAUDE.md.snippet", "codex": "AGENTS.md.snippet", "gemini": "GEMINI.md.snippet"}
INSTRUCTION_NAMES = {"claude": "CLAUDE.md", "codex": "AGENTS.md", "gemini": "GEMINI.md"}
GEMINI_COMMANDS = ("lean.toml", "debug.toml", "spec.toml", "pr.toml", "map.toml")
SHELL_SCRIPTS = ("installers/install.sh", "installers/uninstall.sh", "adapters/claude/hooks/read-guard.sh")
MARKER_START = "agentforge:lean-routing:start"
MARKER_END = "agentforge:lean-routing:end"


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def check_required() -> list[str]:
    return [f"missing {rel}" for rel in REQUIRED if not (ROOT / rel).exists()]


def check_registry() -> list[str]:
    errors: list[str] = []
    for rel in ("registry/skills.json", "registry/platforms.json"):
        try:
            json.loads(read(rel))
        except Exception as exc:
            errors.append(f"invalid {rel}: {exc}")
    return errors


def check_version() -> list[str]:
    version = read("VERSION").strip()
    declared = tomllib.loads(read("pyproject.toml"))["project"]["version"]
    if declared != version:
        return [f"pyproject.toml version {declared} != VERSION {version}"]
    return []


def check_skill_frontmatter() -> list[str]:
    errors: list[str] = []
    for name in SKILLS:
        text = read(f"skills/{name}/SKILL.md")
        if not text.startswith("---\n") or f"name: {name}" not in text:
            errors.append(f"invalid {name} SKILL.md frontmatter")
        else:
            errors.extend(check_description(name, text.split("\n---", 1)[0]))
    return errors


def check_description(name: str, frontmatter: str) -> list[str]:
    match = re.search(r"^description: (.*)$", frontmatter, flags=re.M)
    if not match:
        return [f"{name} SKILL.md has no description"]
    value = match.group(1)
    errors: list[str] = []
    if "Use " not in value:
        errors.append(f"{name} SKILL.md description must say when to use the skill")
    # An unquoted YAML scalar containing ": " is a parse error and makes the skill unloadable.
    if ": " in value and value[0] not in "'\"":
        errors.append(f"{name} SKILL.md description contains ': ' (invalid YAML); quote it or rephrase")
    return errors


def check_skill_links() -> list[str]:
    """Every bundled file must be referenced from SKILL.md, and every link must resolve."""
    errors: list[str] = []
    for name in SKILLS:
        skill_dir = ROOT / "skills" / name
        text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        for path in sorted(skill_dir.rglob("*")):
            rel = path.relative_to(skill_dir).as_posix()
            if path.is_file() and rel != "SKILL.md" and "__pycache__" not in rel and rel not in text:
                errors.append(f"{name}: {rel} is not referenced from SKILL.md")
        links = re.findall(r"\]\(([^)#]+)\)", text)
        errors.extend(f"{name}: broken link {link}" for link in links if not (skill_dir / link).exists())
    return errors


def check_snippets() -> list[str]:
    errors: list[str] = []
    for platform, filename in SNIPPETS.items():
        text = read(f"adapters/{platform}/{filename}")
        if text.count(MARKER_START) != 1 or text.count(MARKER_END) != 1:
            errors.append(f"bad marker block: {platform}")
    return errors


def check_toml() -> list[str]:
    errors: list[str] = []
    for path in (ROOT / "adapters/codex/agents").glob("*.toml"):
        try:
            tomllib.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"invalid TOML {path.relative_to(ROOT)}: {exc}")
    for cmd_file in GEMINI_COMMANDS:
        try:
            tomllib.loads(read(f"adapters/gemini/commands/{cmd_file}"))
        except Exception as exc:
            errors.append(f"invalid Gemini command TOML ({cmd_file}): {exc}")
    return errors


def check_shell_syntax() -> list[str]:
    errors: list[str] = []
    for shell in SHELL_SCRIPTS:
        result = subprocess.run(["bash", "-n", str(ROOT / shell)], capture_output=True, text=True, check=False)
        if result.returncode:
            errors.append(f"shell syntax {shell}: {result.stderr.strip()}")
    return errors


def run_installer(script: str, platform: str, target: Path) -> None:
    subprocess.run(
        ["bash", str(ROOT / f"installers/{script}"), platform, str(target)],
        check=True,
        stdout=subprocess.DEVNULL,
    )


def smoke_test_platform(platform: str, target: Path) -> list[str]:
    """Project install, idempotence, preservation of existing text, and uninstall."""
    errors: list[str] = []
    inst = target / INSTRUCTION_NAMES[platform]
    inst.write_text(f"# Existing {platform} instructions\n\nkeep-me\n", encoding="utf-8")
    run_installer("install.sh", platform, target)
    run_installer("install.sh", platform, target)
    text = inst.read_text(encoding="utf-8")
    if text.count(MARKER_START) != 1:
        errors.append(f"installer not idempotent: {platform}")
    if "keep-me" not in text:
        errors.append(f"installer overwrote existing content: {platform}")
    run_installer("uninstall.sh", platform, target)
    text = inst.read_text(encoding="utf-8") if inst.exists() else ""
    if MARKER_START in text:
        errors.append(f"uninstall marker remained: {platform}")
    if "keep-me" not in text:
        errors.append(f"uninstall removed existing content: {platform}")
    return errors


def check_installers() -> list[str]:
    with tempfile.TemporaryDirectory() as td:
        return [e for platform in INSTRUCTION_NAMES for e in smoke_test_platform(platform, Path(td))]


CHECKS = (
    check_required,
    check_registry,
    check_version,
    check_skill_frontmatter,
    check_skill_links,
    check_snippets,
    check_toml,
    check_shell_syntax,
    check_installers,
)


def main() -> int:
    errors = [error for check in CHECKS for error in check()]
    if errors:
        for error in errors:
            print("FAIL:", error)
        print(f"{len(errors)} validation error(s)")
        return 1

    print("AgentForge validation PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
