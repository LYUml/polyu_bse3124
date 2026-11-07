$ErrorActionPreference = 'Stop'
$latexBin = Join-Path $env:LOCALAPPDATA 'Programs/MiKTeX/miktex/bin/x64'
$taskRoot = (Get-Item -LiteralPath $PSScriptRoot).Parent.Parent.Parent.FullName
$taskPython = Join-Path $taskRoot '.venv/Scripts/python.exe'
& $taskPython (Join-Path $taskRoot '04_Design_Outputs/calculations/build_latex_answer.py')
if ($LASTEXITCODE -ne 0) { throw 'Answer-source generation failed' }
Push-Location $PSScriptRoot
try {
    New-Item -ItemType Directory -Path build -Force | Out-Null
    for ($latexPass = 1; $latexPass -le 2; $latexPass++) {
        & (Join-Path $latexBin 'xelatex.exe') -interaction=batchmode -halt-on-error -file-line-error -output-directory=build main.tex
        if ($LASTEXITCODE -ne 0) { throw 'XeLaTeX compilation failed' }
    }
    $latexIssues = Select-String -LiteralPath build/main.log -Pattern 'Overfull|undefined references|LaTeX Error'
    if ($latexIssues) { $latexIssues; throw 'Review LaTeX layout diagnostics before delivery' }
    Copy-Item -LiteralPath build/main.pdf -Destination ../BSE3124_Answer_Sheets_v02.pdf -Force
} finally {
    Pop-Location
}
