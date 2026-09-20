# PowerShell installer for AgentForge
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
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir

function Run-Action {
    param([string]$Description, [scriptblock]$Action)
    if ($DryRun) {
        Write-Host "[dry-run] $Description"
    } else {
        & $Action
    }
}

function Copy-DirectoryContent {
    param([string]$Src, [string]$Dst)
    if (-not (Test-Path $Src)) { return }
    Run-Action "Copy files from $Src to $Dst" {
        if (-not (Test-Path $Dst)) {
            New-Item -ItemType Directory -Path $Dst -Force | Out-Null
        }
        Get-ChildItem -Path $Src -Recurse | ForEach-Object {
            $rel = $_.FullName.Substring($Src.Length).TrimStart('\', '/')
            $destFile = Join-Path $Dst $rel
            if ($_.PSIsContainer) {
                if (-not (Test-Path $destFile)) {
                    New-Item -ItemType Directory -Path $destFile -Force | Out-Null
                }
            } else {
                $parentDir = Split-Path -Parent $destFile
                if (-not (Test-Path $parentDir)) {
                    New-Item -ItemType Directory -Path $parentDir -Force | Out-Null
                }
                Copy-Item -Path $_.FullName -Destination $destFile -Force
            }
        }
    }
}

function Update-InstructionFile {
    param([string]$FilePath, [string]$SnippetPath)
    if (-not (Test-Path $SnippetPath)) { return }
    $snippet = Get-Content -Path $SnippetPath -Raw -Encoding utf8

    Run-Action "Ensure AgentForge block in $FilePath" {
        $parent = Split-Path -Parent $FilePath
        if ($parent -and -not (Test-Path $parent)) {
            New-Item -ItemType Directory -Path $parent -Force | Out-Null
        }
        $existing = ""
        if (Test-Path $FilePath) {
            $existing = Get-Content -Path $FilePath -Raw -Encoding utf8
        }
        $pattern = "(?s)<!-- agentforge:lean-routing:start -->.*?<!-- agentforge:lean-routing:end -->\r?\n?"
        $cleaned = [regex]::Replace($existing, $pattern, "").TrimEnd()

        $finalContent = if ($cleaned.Length -gt 0) {
            $cleaned + "`r`n`r`n" + $snippet.Trim() + "`r`n"
        } else {
            $snippet.Trim() + "`r`n"
        }
        [System.IO.File]::WriteAllText($FilePath, $finalContent, [System.Text.Encoding]::UTF8)
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

# 1. Copy all portable skills
Get-ChildItem -Path (Join-Path $RepoRoot "skills") -Directory | ForEach-Object {
    $dest = Join-Path $SkillsDir $_.Name
    Copy-DirectoryContent -Src $_.FullName -Dst $dest
}

# 2. Copy adapter-specific agents
Copy-DirectoryContent -Src (Join-Path $RepoRoot "adapters/$Platform/agents") -Dst $AgentsPath

# 3. Update instruction snippet
switch ($Platform) {
    'claude' {
        Update-InstructionFile -FilePath $InstFile -SnippetPath (Join-Path $RepoRoot "adapters/claude/CLAUDE.md.snippet")
    }
    'codex' {
        Update-InstructionFile -FilePath $InstFile -SnippetPath (Join-Path $RepoRoot "adapters/codex/AGENTS.md.snippet")
    }
    'gemini' {
        Update-InstructionFile -FilePath $InstFile -SnippetPath (Join-Path $RepoRoot "adapters/gemini/GEMINI.md.snippet")
        Copy-DirectoryContent -Src (Join-Path $RepoRoot "adapters/gemini/commands") -Dst $CmdsPath
    }
}

Write-Host "AgentForge installed for $Platform"
Write-Host "Skills: $SkillsDir"
Write-Host "Agents: $AgentsPath"
Write-Host "Instructions: $InstFile"
