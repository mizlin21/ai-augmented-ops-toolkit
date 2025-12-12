Write-Host "====================================="
Write-Host " AI-Augmented System Operations Toolkit"
Write-Host "====================================="

Write-Host ""
Write-Host "[INFO] Starting system checks..."
Write-Host ""

# Move to repo root (in case script is run from elsewhere)
$repoRoot = Resolve-Path "$PSScriptRoot\.."
Set-Location $repoRoot

# Run the main orchestration
python -m src.main

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "[ERROR] One or more checks failed to run."
    exit 1
}

Write-Host ""
Write-Host "[INFO] All checks completed."
