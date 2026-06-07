#!/usr/bin/env pwsh
<#
.SYNOPSIS
Generate a spec using Claude Opus and save it to spec/inprogress/

.PARAMETER Title
The spec title

.PARAMETER Description
Brief description of what to spec
#>

param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$Title,

    [Parameter(Mandatory=$true, Position=1)]
    [string]$Description
)

# Check for API key
if (-not $env:ANTHROPIC_API_KEY) {
    Write-Error "ANTHROPIC_API_KEY environment variable not set"
    exit 1
}

$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$slug = $Title -replace '[^a-zA-Z0-9]', '-' -replace '-+', '-' | % { $_.ToLower().Trim('-') }

# Prompt for clarifications
Write-Host "Clarifying questions for spec: $Title" -ForegroundColor Cyan
$audience = Read-Host "Who is the primary user/audience for this?"
$scope = Read-Host "What is the scope? (e.g., 'single level', 'full game system', 'menu flow')"

# Build system prompt for game spec generation
$systemPrompt = @"
You are a game design spec expert. Generate detailed, practical game specs.

For the game in question, create a comprehensive spec that includes:
1. **Overview** - Concise description of the feature/mechanic
2. **Core Mechanics** - How it works, what the player does
3. **Requirements** - What must be true for this to function
4. **Acceptance Criteria** - How to know when it's complete
5. **Technical Considerations** - Architecture, asset requirements, implementation complexity
6. **Edge Cases** - Unusual scenarios to handle
7. **Dependencies** - What this relies on
8. **Implementation Notes** - Suggestions for how to approach building this

Write in clear, actionable language. Be specific. Include examples where helpful.
"@

# Build the user message
$userMessage = @"
Create a spec for: **$Title**

Description: $Description

Target audience/player: $audience
Scope: $scope

Generate a complete spec in markdown format.
"@

# Call Claude Opus
$body = @{
    model = "claude-opus-4-8"
    max_tokens = 2000
    system = $systemPrompt
    messages = @(
        @{
            role = "user"
            content = $userMessage
        }
    )
} | ConvertTo-Json -Depth 10

Write-Host "Generating spec with Claude Opus..." -ForegroundColor Green

$response = Invoke-RestMethod `
    -Uri "https://api.anthropic.com/v1/messages" `
    -Method POST `
    -Headers @{
        "x-api-key" = $env:ANTHROPIC_API_KEY
        "anthropic-version" = "2023-06-01"
        "content-type" = "application/json"
    } `
    -Body $body

if ($response.content[0].type -ne "text") {
    Write-Error "Unexpected response type: $($response.content[0].type)"
    exit 1
}

$specContent = $response.content[0].text

# Write to file
$outputDir = "spec/inprogress"
$outputFile = "$outputDir/$slug.md"

# Add header with metadata
$fileContent = @"
# $Title

**Created**: $timestamp
**Status**: In Progress
**Audience**: $audience
**Scope**: $scope

---

$specContent
"@

Set-Content -Path $outputFile -Value $fileContent -Encoding UTF8

Write-Host "Spec created: $outputFile" -ForegroundColor Green
Write-Host ""
Get-Content $outputFile | head -20
Write-Host "..."
Write-Host "(Full spec saved to $outputFile)"
