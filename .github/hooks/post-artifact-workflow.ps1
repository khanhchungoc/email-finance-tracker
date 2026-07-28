$inputText = [Console]::In.ReadToEnd()
if ([string]::IsNullOrWhiteSpace($inputText)) {
    exit 0
}

try {
    $payload = $inputText | ConvertFrom-Json
} catch {
    Write-Error "Unable to parse hook input as JSON: $($_.Exception.Message)"
    exit 2
}

$toolInput = $payload.toolInput
$paths = @(
    [string]$toolInput.filePath,
    [string]$toolInput.path,
    [string]$toolInput.oldPath,
    [string]$toolInput.newPath
) | Where-Object { $_ -and $_ -ne "" }

$artifactPaths = $paths | Where-Object {
    $_ -match '(^|[\\/])requirements[\\/]output[\\/]' -or
    $_ -match '(^|[\\/])project-knowledge-base[\\/]'
}

if (-not $artifactPaths) {
    exit 0
}

$normalizedPaths = $artifactPaths -replace '\\', '/'
$requirementsChanged = $normalizedPaths | Where-Object { $_ -match '(^|/)requirements/output/' }
$knowledgeChanged = $normalizedPaths | Where-Object { $_ -match '(^|/)project-knowledge-base/' }
$messages = @()

if ($requirementsChanged) {
    $messages += 'Run the manage-requirement-artifacts post-write checklist: sync the nearest index.md and related traceability links.'
}
if ($knowledgeChanged) {
    $messages += 'Run the update-project-knowledge post-write checklist: sync the nearest index.md and log.md; update the root index only when required.'
}

[Console]::WriteLine((@{ systemMessage = ($messages -join ' ') } | ConvertTo-Json -Compress))
exit 0
