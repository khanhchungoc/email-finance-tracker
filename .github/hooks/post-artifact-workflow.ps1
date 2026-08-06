$inputText = [Console]::In.ReadToEnd()
if ([string]::IsNullOrWhiteSpace($inputText)) { exit 0 }
try { $payload = $inputText | ConvertFrom-Json } catch { exit 2 }

$paths = @([string]$payload.toolInput.filePath, [string]$payload.toolInput.path, [string]$payload.toolInput.oldPath, [string]$payload.toolInput.newPath, [string]$payload.toolInput.TargetFile) | Where-Object { $_ -and $_ -ne "" }
$messages = @()

$artifactPaths = $paths | Where-Object { $_ -match '(^|[\\/])requirements[\\/]' -or $_ -match '(^|[\\/])project-knowledge-base[\\/]' }
if (-not $artifactPaths) { exit 0 }

$normalizedPaths = $paths -replace '\\', '/'
$reqs = $normalizedPaths | Where-Object { $_ -match '(^|/)requirements/' }
$kb = $normalizedPaths | Where-Object { $_ -match '(^|/)project-knowledge-base/' }

if ($reqs) {
    $messages += 'Sync nearest index.md and traceability links.'
    foreach ($path in $reqs) {
        if (Test-Path $path) {
            if ($path -match '\.bpmn$') {
                try {
                    node .github/skills/generate-diagram/scripts/autolayout_bpmn.js "$path"
                    $messages += "Auto-layout & post-processing completed for $path."
                } catch {
                    $messages += "Auto-layout failed for $path."
                }
            }
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



