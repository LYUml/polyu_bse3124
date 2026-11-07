$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
$env:AUTOCAD_MCP_BACKEND = 'com'
$env:CAD_LAUNCH = 'never'
$env:ALLOWED_PATHS = Join-Path $projectRoot '04_Design_Outputs'
$env:DANGEROUS_COMMANDS_ENABLED = 'false'
$env:LISP_POLICY = 'read'
$env:ACADMCP_STATE_DIR = Join-Path $projectRoot '04_Design_Outputs/mcp_state'
& (Join-Path $projectRoot '.venv/Scripts/autocad-mcp.exe')
