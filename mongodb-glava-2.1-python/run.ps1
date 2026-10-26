# PowerShell script for running examples of Chapter 2.1
param(
    [string]$File = "all"
)

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "   MongoDB Chapter 2.1 - Python Examples" -ForegroundColor Cyan
Write-Host "========================================================`n" -ForegroundColor Cyan

if ($File -eq "all") {
    Get-ChildItem -Path (Join-Path $PSScriptRoot "primery\*.py") | Sort-Object Name | ForEach-Object {
        Write-Host "── $($_.Name) ──" -ForegroundColor Yellow
        python $_.FullName
        Write-Host ""
    }
} else {
    $target = if (Test-Path $File) { $File } else { Join-Path $PSScriptRoot "primery\$File" }
    if (Test-Path $target) {
        Write-Host "── $(Split-Path $target -Leaf) ──" -ForegroundColor Yellow
        python $target
    } else {
        Write-Host "File not found: $target" -ForegroundColor Red
    }
}

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "Done." -ForegroundColor Green
