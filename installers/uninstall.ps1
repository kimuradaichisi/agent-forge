# PowerShell uninstaller for AgentForge
[CmdletBinding()]
param (
    [Parameter(Mandatory = $true, Position = 0)]
    [ValidateSet('claude', 'codex', 'gemini')]
    [string]$Platform,

    [Parameter(Position = 1)]
    [string]$Target = '.',

    [switch]$Global,
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'

function Run-Action {
    param([string]$Description, [scriptblock]$Action)
    if ($DryRun) {
        Write-Host "[dry-run] $Description"
    } else {
        & $Action
    }
}

function Remove-PathSafe {
    param([string]$PathToRemove)
    if (Test-Path $PathToRemove) {
        Run-Action "Remove $PathToRemove" {
            Remove-Item -Path $PathToRemove -Recurse -Force -ErrorAction SilentlyContinue
        }
    }
}

function Clean-InstructionFile {
    param([string]$FilePath)
    if (Test-Path $FilePath) {
        if ($DryRun) {
            Write-Host "[dry-run] remove AgentForge block from $FilePath"
            return
        }
        $existing = Get-Content -Path $FilePath -Raw -Encoding utf8
        $pattern = "(?s)<!-- agentforge:lean-routing:start -->.*?<!-- agentforge:lean-routing:end -->\r?\n?"
        $cleaned = [regex]::Replace($existing, $pattern, "").TrimEnd()

        if ($cleaned.Length -gt 0) {
            [System.IO.File]::WriteAllText($FilePath, $cleaned + "`r`n", [System.Text.Encoding]::UTF8)
        } else {
            Remove-Item -Path $FilePath -Force -ErrorAction SilentlyContinue
        }
    }
}

$HomeDir = if ($IsWindows -or $env:OS -like "*Windows*") { $env:USERPROFILE } else { $env:HOME }

if ($Global) {
    switch ($Platform) {
        'claude' {
            $SkillsDir = Join-Path $HomeDir ".claude/skills"
            $AgentsPath = Join-Path $HomeDir ".claude/agents"
            $InstFile = Join-Path $HomeDir ".claude/CLAUDE.md"
        }
        'codex' {
            $SkillsDir = Join-Path $HomeDir ".agents/skills"
            $AgentsPath = Join-Path $HomeDir ".codex/agents"
            $InstFile = Join-Path $HomeDir ".codex/AGENTS.md"
        }
        'gemini' {
            $SkillsDir = Join-Path $HomeDir ".agents/skills"
            $AgentsPath = Join-Path $HomeDir ".gemini/agents"
            $InstFile = Join-Path $HomeDir ".gemini/GEMINI.md"
            $CmdsPath = Join-Path $HomeDir ".gemini/commands"
        }
    }
} else {
    $ResolvedTarget = if (Test-Path $Target) { (Resolve-Path $Target).Path } else { [System.IO.Path]::GetFullPath($Target) }
    switch ($Platform) {
        'claude' {
            $SkillsDir = Join-Path $ResolvedTarget ".claude/skills"
            $AgentsPath = Join-Path $ResolvedTarget ".claude/agents"
            $InstFile = Join-Path $ResolvedTarget "CLAUDE.md"
        }
        'codex' {
            $SkillsDir = Join-Path $ResolvedTarget ".agents/skills"
            $AgentsPath = Join-Path $ResolvedTarget ".codex/agents"
            $InstFile = Join-Path $ResolvedTarget "AGENTS.md"
        }
        'gemini' {
            $SkillsDir = Join-Path $ResolvedTarget ".agents/skills"
            $AgentsPath = Join-Path $ResolvedTarget ".gemini/agents"
            $InstFile = Join-Path $ResolvedTarget "GEMINI.md"
            $CmdsPath = Join-Path $ResolvedTarget ".gemini/commands"
        }
    }
}

# 1. Remove skill directories
Remove-PathSafe -PathToRemove (Join-Path $SkillsDir "lean-routing")
Remove-PathSafe -PathToRemove (Join-Path $SkillsDir "scientific-debugging")

# 2. Remove agent files
switch ($Platform) {
    'claude' {
        foreach ($f in @('cheap-ops.md', 'cheap-edit.md', 'cheap-coder.md', 'reviewer.md')) {
            Remove-PathSafe -PathToRemove (Join-Path $AgentsPath $f)
        }
    }
    'codex' {
        foreach ($f in @('cheap_ops.toml', 'cheap_edit.toml', 'cheap_coder.toml', 'reviewer.toml')) {
            Remove-PathSafe -PathToRemove (Join-Path $AgentsPath $f)
        }
    }
    'gemini' {
        foreach ($f in @('cheap-ops.md', 'cheap-edit.md', 'cheap-coder.md', 'reviewer.md')) {
            Remove-PathSafe -PathToRemove (Join-Path $AgentsPath $f)
        }
        Remove-PathSafe -PathToRemove (Join-Path $CmdsPath "lean.toml")
        Remove-PathSafe -PathToRemove (Join-Path $CmdsPath "debug.toml")
    }
}

# 3. Clean instruction file
Clean-InstructionFile -FilePath $InstFile

Write-Host "AgentForge removed for $Platform. Unrelated files were left untouched."
