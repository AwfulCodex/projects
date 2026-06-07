#!/usr/bin/env pwsh
<#
.SYNOPSIS
Move a spec from inprogress to completed

.PARAMETER SpecName
The name of the spec file (without .md extension)
#>

param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$SpecName
)

$specFile = "spec/inprogress/$SpecName.md"

if (-not (Test-Path $specFile)) {
    Write-Error "Spec not found: $specFile"
    exit 1
}

# Read and update status
$content = Get-Content $specFile -Raw
$content = $content -replace 'Status.*: In Progress', 'Status: Completed'
$content = $content -replace '(?<=Completed:?\*\*)', " $(Get-Date -Format 'yyyy-MM-dd')"

# Write to completed
$completedFile = "spec/completed/$SpecName.md"
Set-Content -Path $completedFile -Value $content -Encoding UTF8

# Remove from in-progress
Remove-Item $specFile

Write-Host "Spec moved to completed: $completedFile" -ForegroundColor Green
