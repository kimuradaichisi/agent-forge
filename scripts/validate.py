#!/usr/bin/env python3
from pathlib import Path
import json
import subprocess
import tempfile
import tomllib

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    'README.md', 'LICENSE', 'VERSION',
    'registry/skills.json', 'registry/platforms.json',
    'skills/lean-routing/SKILL.md',
    'skills/scientific-debugging/SKILL.md',
    'skills/spec-driven-dev/SKILL.md',
    'skills/pr-guardian/SKILL.md',
    'skills/codebase-cartographer/SKILL.md',
    'installers/install.sh', 'installers/uninstall.sh',
    'installers/install.ps1', 'installers/uninstall.ps1',
    'adapters/claude/CLAUDE.md.snippet',
    'adapters/codex/AGENTS.md.snippet',
    'adapters/gemini/GEMINI.md.snippet',
]


def main() -> int:
    errors: list[str] = []

    for rel in REQUIRED:
        if not (ROOT / rel).exists():
            errors.append(f'missing {rel}')

    for rel in ('registry/skills.json', 'registry/platforms.json'):
        try:
            json.loads((ROOT / rel).read_text(encoding='utf-8'))
        except Exception as exc:
            errors.append(f'invalid {rel}: {exc}')

    skill = (ROOT / 'skills/lean-routing/SKILL.md').read_text(encoding='utf-8')
    if not skill.startswith('---\n') or 'name: lean-routing' not in skill:
        errors.append('invalid lean-routing SKILL.md frontmatter')

    debug_skill = (ROOT / 'skills/scientific-debugging/SKILL.md').read_text(encoding='utf-8')
    if not debug_skill.startswith('---\n') or 'name: scientific-debugging' not in debug_skill:
        errors.append('invalid scientific-debugging SKILL.md frontmatter')

    spec_skill = (ROOT / 'skills/spec-driven-dev/SKILL.md').read_text(encoding='utf-8')
    if not spec_skill.startswith('---\n') or 'name: spec-driven-dev' not in spec_skill:
        errors.append('invalid spec-driven-dev SKILL.md frontmatter')

    pr_skill = (ROOT / 'skills/pr-guardian/SKILL.md').read_text(encoding='utf-8')
    if not pr_skill.startswith('---\n') or 'name: pr-guardian' not in pr_skill:
        errors.append('invalid pr-guardian SKILL.md frontmatter')

    cart_skill = (ROOT / 'skills/codebase-cartographer/SKILL.md').read_text(encoding='utf-8')
    if not cart_skill.startswith('---\n') or 'name: codebase-cartographer' not in cart_skill:
        errors.append('invalid codebase-cartographer SKILL.md frontmatter')

    snippets = {
        'claude': 'CLAUDE.md.snippet',
        'codex': 'AGENTS.md.snippet',
        'gemini': 'GEMINI.md.snippet',
    }
    for platform, filename in snippets.items():
        text = (ROOT / f'adapters/{platform}/{filename}').read_text(encoding='utf-8')
        if text.count('agentforge:lean-routing:start') != 1 or text.count('agentforge:lean-routing:end') != 1:
            errors.append(f'bad marker block: {platform}')

    for path in (ROOT / 'adapters/codex/agents').glob('*.toml'):
        try:
            tomllib.loads(path.read_text(encoding='utf-8'))
        except Exception as exc:
            errors.append(f'invalid TOML {path.relative_to(ROOT)}: {exc}')

    for cmd_file in ('lean.toml', 'debug.toml', 'spec.toml', 'pr.toml', 'map.toml'):
        try:
            tomllib.loads((ROOT / f'adapters/gemini/commands/{cmd_file}').read_text(encoding='utf-8'))
        except Exception as exc:
            errors.append(f'invalid Gemini command TOML ({cmd_file}): {exc}')

    for shell in ('installers/install.sh', 'installers/uninstall.sh', 'adapters/claude/hooks/read-guard.sh'):
        result = subprocess.run(['bash', '-n', str(ROOT / shell)], capture_output=True, text=True)
        if result.returncode:
            errors.append(f'shell syntax {shell}: {result.stderr.strip()}')

    # Smoke-test project install, idempotence, preservation of existing text, and uninstall.
    with tempfile.TemporaryDirectory() as td:
        target = Path(td)
        instruction_names = {'claude': 'CLAUDE.md', 'codex': 'AGENTS.md', 'gemini': 'GEMINI.md'}
        for platform in ('claude', 'codex', 'gemini'):
            inst = target / instruction_names[platform]
            inst.write_text(f'# Existing {platform} instructions\n\nkeep-me\n', encoding='utf-8')
            subprocess.run(['bash', str(ROOT / 'installers/install.sh'), platform, str(target)], check=True, stdout=subprocess.DEVNULL)
            subprocess.run(['bash', str(ROOT / 'installers/install.sh'), platform, str(target)], check=True, stdout=subprocess.DEVNULL)
            text = inst.read_text(encoding='utf-8')
            if text.count('agentforge:lean-routing:start') != 1:
                errors.append(f'installer not idempotent: {platform}')
            if 'keep-me' not in text:
                errors.append(f'installer overwrote existing content: {platform}')
            subprocess.run(['bash', str(ROOT / 'installers/uninstall.sh'), platform, str(target)], check=True, stdout=subprocess.DEVNULL)
            text = inst.read_text(encoding='utf-8') if inst.exists() else ''
            if 'agentforge:lean-routing:start' in text:
                errors.append(f'uninstall marker remained: {platform}')
            if 'keep-me' not in text:
                errors.append(f'uninstall removed existing content: {platform}')

    if errors:
        for error in errors:
            print('FAIL:', error)
        print(f'{len(errors)} validation error(s)')
        return 1

    print('AgentForge validation PASS')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
