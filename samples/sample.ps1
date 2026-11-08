# Sample PowerShell code to test Bluloco Dark
function Get-ThemeInfo {
    param (
        [string]$Path
    )
    if (Test-Path $Path) {
        Write-Host "File $Path exists" -ForegroundColor Cyan
        Get-Content $Path | Select-Object -First 10
    } else {
        Write-Error "File not found"
    }
}

$files = Get-ChildItem -Path .\samples -Filter *.xml
foreach ($file in $files) {
    Get-ThemeInfo -Path $file.FullName
}
