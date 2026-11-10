$ErrorActionPreference = 'Stop'
$latexExe = Join-Path $env:LOCALAPPDATA 'Programs/MiKTeX/miktex/bin/x64/xelatex.exe'
Push-Location $PSScriptRoot
try {
    New-Item -ItemType Directory -Path build -Force | Out-Null
    for ($pass = 1; $pass -le 2; $pass++) {
        & $latexExe -interaction=batchmode -halt-on-error -output-directory=build main.tex
        if ($LASTEXITCODE -ne 0) { throw 'XeLaTeX compilation failed' }
    }
    if (Select-String -LiteralPath build/main.log -Pattern 'Overfull|undefined references|LaTeX Error') { throw 'Review layout diagnostics' }
    & (Join-Path $PSScriptRoot "../../../.venv/Scripts/python.exe") finalize_pdf.py
    if ($LASTEXITCODE -ne 0) { throw 'PDF finalization failed' }
} finally { Pop-Location }
