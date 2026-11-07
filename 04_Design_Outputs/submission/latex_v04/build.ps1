$ErrorActionPreference = 'Stop'
$taskRoot = (Get-Item -LiteralPath $PSScriptRoot).Parent.Parent.Parent.FullName
$taskPython = Join-Path $taskRoot '.venv/Scripts/python.exe'
$latexExe = Join-Path $env:LOCALAPPDATA 'Programs/MiKTeX/miktex/bin/x64/xelatex.exe'
& $taskPython (Join-Path $taskRoot '04_Design_Outputs/calculations/final_lighting_basis.py')
if ($LASTEXITCODE -ne 0) { throw 'Photometry calculation failed' }
& $taskPython (Join-Path $taskRoot '04_Design_Outputs/calculations/fault_protection_design.py')
if ($LASTEXITCODE -ne 0) { throw 'Protection calculation failed' }
& $taskPython (Join-Path $taskRoot '04_Design_Outputs/calculations/build_answer_v04.py')
if ($LASTEXITCODE -ne 0) { throw 'Source generation failed' }
Push-Location $PSScriptRoot
try {
    New-Item -ItemType Directory -Path build -Force | Out-Null
    foreach ($source in @('main.tex','template_blank.tex')) {
        for ($pass = 1; $pass -le 2; $pass++) {
            & $latexExe -interaction=batchmode -halt-on-error -output-directory=build $source
            if ($LASTEXITCODE -ne 0) { throw "Compilation failed: $source" }
        }
        $log = Join-Path build ([IO.Path]::GetFileNameWithoutExtension($source) + '.log')
        if (Select-String -LiteralPath $log -Pattern 'Overfull|undefined references|LaTeX Error') { throw 'Layout diagnostics require review' }
    }
    Copy-Item -LiteralPath build/main.pdf -Destination ../BSE3124_Answer_Sheets_v04.pdf -Force
    Copy-Item -LiteralPath build/template_blank.pdf -Destination ../BSE3124_Template_LaTeX.pdf -Force
} finally { Pop-Location }
