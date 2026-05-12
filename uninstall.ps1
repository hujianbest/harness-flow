#requires -Version 5.1
<#
.SYNOPSIS
    HarnessFlow uninstall.sh — Windows / PowerShell wrapper.

.DESCRIPTION
    Mirror of install.ps1 for the uninstall side. Locates a usable bash
    interpreter (Git Bash → bash on PATH → WSL), translates --host to a POSIX
    path, and forwards all arguments to uninstall.sh.

    All flag semantics (--host, --dry-run) come from uninstall.sh; run
    `pwsh -File uninstall.ps1 --help` to see them.

.EXAMPLE
    pwsh -File uninstall.ps1 --host C:\src\my-project
#>

[CmdletBinding(PositionalBinding = $false)]
param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]] $ScriptArgs
)

$ErrorActionPreference = 'Stop'

function Write-Err {
    param([string] $Message)
    [Console]::Error.WriteLine("[hf-uninstall][ERROR] $Message")
}

function ConvertTo-PosixPath {
    param([string] $WinPath)
    if ([string]::IsNullOrEmpty($WinPath)) { return $WinPath }
    $resolved = $WinPath
    try {
        $rp = Resolve-Path -LiteralPath $WinPath -ErrorAction Stop
        $resolved = $rp.Path
    } catch {
        $resolved = $WinPath
    }
    if ($resolved -match '^([A-Za-z]):[\\/](.*)$') {
        $drive = $Matches[1].ToLower()
        $rest = $Matches[2] -replace '\\', '/'
        return "/$drive/$rest"
    }
    return $resolved -replace '\\', '/'
}

function Test-BashCandidate {
    param([string] $Path)
    if ([string]::IsNullOrEmpty($Path)) { return $false }
    try {
        return Test-Path -LiteralPath $Path
    } catch {
        return $false
    }
}

function Find-BashInterpreter {
    $roots = @(
        $env:ProgramFiles,
        ${env:ProgramFiles(x86)},
        $env:LocalAppData,
        'C:\Program Files',
        'C:\Program Files (x86)'
    )
    $relatives = @('\Git\bin\bash.exe', '\Programs\Git\bin\bash.exe')
    foreach ($root in $roots) {
        if ([string]::IsNullOrEmpty($root)) { continue }
        foreach ($rel in $relatives) {
            $candidate = "$root$rel"
            if (Test-BashCandidate $candidate) {
                return [pscustomobject]@{ Type = 'gitbash'; Path = $candidate }
            }
        }
    }
    $cmd = Get-Command bash -ErrorAction SilentlyContinue
    if ($cmd) {
        return [pscustomobject]@{ Type = 'gitbash'; Path = $cmd.Source }
    }
    $wsl = Get-Command wsl -ErrorAction SilentlyContinue
    if ($wsl) {
        return [pscustomobject]@{ Type = 'wsl'; Path = $wsl.Source }
    }
    return $null
}

function Convert-Args {
    param([string[]] $InputArgs)
    if (-not $InputArgs) { return @() }
    $out = New-Object System.Collections.Generic.List[string]
    for ($i = 0; $i -lt $InputArgs.Count; $i++) {
        $a = $InputArgs[$i]
        if ($a -eq '--host' -and ($i + 1) -lt $InputArgs.Count) {
            $out.Add('--host')
            $out.Add((ConvertTo-PosixPath $InputArgs[$i + 1]))
            $i++
            continue
        }
        if ($a -like '--host=*') {
            $val = $a.Substring('--host='.Length)
            $out.Add('--host=' + (ConvertTo-PosixPath $val))
            continue
        }
        $out.Add($a)
    }
    return $out.ToArray()
}

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$bashScript = Join-Path $scriptDir 'uninstall.sh'
if (-not (Test-Path -LiteralPath $bashScript)) {
    Write-Err "uninstall.sh not found next to uninstall.ps1 (looked at: $bashScript)"
    exit 1
}

$bash = Find-BashInterpreter
if (-not $bash) {
    Write-Err @"
HarnessFlow uninstall requires a POSIX bash interpreter. None of these were found:
  - Git for Windows (Git Bash):  https://git-scm.com/download/win
  - WSL:                         wsl --install
  - MSYS2:                       https://www.msys2.org/

After installing one of the above, retry:
  pwsh -File uninstall.ps1 $($ScriptArgs -join ' ')

Or open Git Bash directly and run:
  bash uninstall.sh $($ScriptArgs -join ' ')
"@
    exit 1
}

$forwarded = Convert-Args -InputArgs $ScriptArgs

if ($bash.Type -eq 'wsl') {
    $bashScriptPosix = (& wsl wslpath -u "$bashScript").Trim()
    & wsl bash $bashScriptPosix @forwarded
} else {
    $bashScriptPosix = ConvertTo-PosixPath $bashScript
    & $bash.Path $bashScriptPosix @forwarded
}

exit $LASTEXITCODE
