$inputText = [Console]::In.ReadToEnd()
if ([string]::IsNullOrWhiteSpace($inputText)) { exit 0 }
try { $payload = $inputText | ConvertFrom-Json } catch { exit 2 }

$paths = @([string]$payload.toolInput.filePath, [string]$payload.toolInput.path, [string]$payload.toolInput.oldPath, [string]$payload.toolInput.newPath) | Where-Object { $_ -and $_ -ne "" }
$artifactPaths = $paths | Where-Object { $_ -match '(^|[\\/])requirements[\\/]output[\\/]' -or $_ -match '(^|[\\/])project-knowledge-base[\\/]' }
if (-not $artifactPaths) { exit 0 }

$normalizedPaths = $artifactPaths -replace '\\', '/'
$reqs = $normalizedPaths | Where-Object { $_ -match '(^|/)requirements/output/' }
$kb = $normalizedPaths | Where-Object { $_ -match '(^|/)project-knowledge-base/' }
$messages = @()

if ($reqs) {
    $messages += 'Sync nearest index.md and traceability links.'
    foreach ($path in $reqs) {
        if (Test-Path $path) {
            $content = Get-Content -Path $path -Raw
            if ($content -match '(?i)status:\s*signed-off') { $messages += 'Signed-off story updated: run update-project-knowledge.' }
            if ($path -match '\.md$' -and $content -notmatch '(?m)^status:') { $messages += 'Missing status frontmatter. Please add.' }
            if ($content -match '(?i)\b(workflow|state change|sequence|complex flow)\b') { $messages += 'Complex logic detected: consider generate-diagram.' }
        }
    }
}
if ($kb) {
    $messages += 'Sync project knowledge indexes.'
}

$uniqueMessages = $messages | Select-Object -Unique
if ($uniqueMessages) { [Console]::WriteLine((@{ systemMessage = ($uniqueMessages -join ' ') } | ConvertTo-Json -Compress)) }
exit 0
