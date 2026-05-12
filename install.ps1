#requires -Version 5.1
<#
.SYNOPSIS
    HarnessFlow install.sh — Windows / PowerShell wrapper.

.DESCRIPTION
    install.sh is a bash 3.2+ script. It runs natively on Linux, macOS, and on
    Windows under Git Bash / WSL / MSYS2, but cannot be invoked directly from
    PowerShell or cmd. This wrapper:

      1. Locates a usable bash interpreter (Git Bash → bash on PATH → WSL).
      2. Converts any Windows-style --host path (e.g. C:\path\to\proj) to a
         POSIX path the bash script can `cd` into.
      3. Forwards all remaining arguments to install.sh unchanged and exits
         with the underlying script's exit code.

    All flag semantics (--target, --topology, --host, --dry-run, --verbose,
    --force) come from install.sh; run `pwsh -File install.ps1 --help` to see
    them.

.NOTES
    Symlink topology (--topology symlink) on Windows requires either Developer
    Mode enabled (Settings → Privacy & security → For developers) or running
    PowerShell elevated. Without it, `ln -s` under Git Bash silently degrades
    to a copy. Default --topology copy works without any of that.

.EXAMPLE
    pwsh -File install.ps1 --target opencode --host C:\src\my-project

.EXAMPLE
    pwsh -File install.ps1 --target both --topology symlink --host .
#>

[CmdletBinding(PositionalBinding = $false)]
param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]] $ScriptArgs
)

$ErrorActionPreference = 'Stop'

function Write-Err {
    param([string] $Message)
    [Console]::Error.WriteLine("[hf-install][ERROR] $Message")
}

function ConvertTo-PosixPath {
    param([string] $WinPath)
    if ([string]::IsNullOrEmpty($WinPath)) { return $WinPath }
    $resolved = $WinPath
    try {
        $rp = Resolve-Path -LiteralPath $WinPath -ErrorAction Stop
        $resolved = $rp.Path
    } catch {
        # Resolve-Path fails for not-yet-existing paths; install.sh itself
        # validates --host existence, so we just normalize what was given.
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
$bashScript = Join-Path $scriptDir 'install.sh'
if (-not (Test-Path -LiteralPath $bashScript)) {
    Write-Err "install.sh not found next to install.ps1 (looked at: $bashScript)"
    exit 1
}

$bash = Find-BashInterpreter
if (-not $bash) {
    Write-Err @"
HarnessFlow install requires a POSIX bash interpreter. None of these were found:
  - Git for Windows (Git Bash):  https://git-scm.com/download/win
  - WSL:                         wsl --install
  - MSYS2:                       https://www.msys2.org/

After installing one of the above, retry:
  pwsh -File install.ps1 $($ScriptArgs -join ' ')

Or open Git Bash directly and run:
  bash install.sh $($ScriptArgs -join ' ')
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
