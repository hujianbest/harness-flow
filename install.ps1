param(
    [ValidateSet("cursor", "opencode", "both")]
    [string] $Target = "both",
    [Parameter(Mandatory = $true)]
    [string] $Dest,
    [ValidateSet("copy", "symlink")]
    [string] $Mode = "copy"
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
& python (Join-Path $ScriptDir "scripts/install.py") --target $Target --dest $Dest --mode $Mode
exit $LASTEXITCODE
