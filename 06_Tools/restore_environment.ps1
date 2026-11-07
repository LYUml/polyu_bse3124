param([Parameter(Mandatory=$true)][string]$PythonExe)
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
Set-Location -LiteralPath $projectRoot
if (-not (Test-Path -LiteralPath '06_Tools/autocad-mcp')) {
    git clone https://github.com/U-C4N/Autocad-MCP.git 06_Tools/autocad-mcp
    if ($LASTEXITCODE -ne 0) { throw 'Clone failed' }
    git -C 06_Tools/autocad-mcp checkout 6f6a538255ca9f885232e845ac32f10b4433fe3e
    if ($LASTEXITCODE -ne 0) { throw 'Pinned checkout failed' }
}
& $PythonExe -m venv .venv
if ($LASTEXITCODE -ne 0) { throw 'venv failed; use Python 3.12' }
& .venv/Scripts/python.exe -m pip install -r 06_Tools/requirements.lock.txt
if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed' }
& .venv/Scripts/python.exe -m pip check
if ($LASTEXITCODE -ne 0) { throw 'Dependency check failed' }
Write-Output 'Environment restored. If workspace moved, update absolute paths in .codex/config.toml.'
