$inputText = [Console]::In.ReadToEnd()
if ([string]::IsNullOrWhiteSpace($inputText)) { exit 0 }
try { $payload = $inputText | ConvertFrom-Json } catch { exit 2 }

# Filter out non-write tools to avoid execution latency on read operations
$writeTools = @('write_to_file', 'replace_file_content', 'multi_replace_file_content')
$toolName = if ($payload.tool) { $payload.tool } elseif ($payload.name) { $payload.name } elseif ($payload.toolName) { $payload.toolName } else { "" }
if ($toolName -and ($writeTools -notcontains $toolName)) { exit 0 }

# Extract and normalize candidate paths
$paths = @([string]$payload.toolInput.TargetFile, [string]$payload.toolInput.filePath, [string]$payload.toolInput.path, [string]$payload.toolInput.oldPath, [string]$payload.toolInput.newPath) | Where-Object { $_ -and $_ -ne "" }
$artifactPaths = $paths | Where-Object { $_ -match '(^|[\\/])requirements[\\/]' -or $_ -match '(^|[\\/])project-knowledge-base[\\/]' -or $_ -match '(^|[\\/])\.agent-artifacts[\\/]' }
if (-not $artifactPaths) { exit 0 }

$messages = @()
$repoRoot = (Resolve-Path "$PSScriptRoot/../..").Path

foreach ($rawPath in $artifactPaths) {
    $normalized = $rawPath -replace '\\', '/'
    
    # Process requirement deliverables
    if ($normalized -match '(^|/)requirements/' -or $normalized -match '(^|/)\.agent-artifacts/requirements/') {
        $messages += 'Sync nearest index.md and traceability links under .agent-artifacts/requirements/output/.'
        
        if (Test-Path $rawPath) {
            # Auto-layout for BPMN diagram XML files
            if ($normalized -match '\.bpmn$') {
                $scriptPath = Join-Path $repoRoot ".github/skills/generate-diagram/scripts/autolayout_bpmn.js"
                if (Test-Path $scriptPath) {
                    try {
                        node "$scriptPath" "$rawPath"
                        $messages += "Auto-layout & post-processing completed for ${rawPath}."
                    } catch {
                        $messages += "Auto-layout script failed for ${rawPath}."
                    }
                }
            }
            
            # Markdown content quality rules (excluding index.md navigation files)
            if ($normalized -match '\.md$' -and $normalized -notmatch '/index\.md$') {
                $content = Get-Content -Path $rawPath -Raw
                if ($content -match '(?i)status:\s*signed-off') { 
                    $messages += "Signed-off story updated (${rawPath}): run update-project-knowledge to distill durable facts into .agent-artifacts/project-knowledge-base/." 
                }
                if ($content -notmatch '(?m)^status:') { 
                    $messages += "Missing 'status:' frontmatter in ${rawPath}. Please add status frontmatter." 
                }
                if ($content -match '(?i)\b(workflow|state change|sequence|complex flow)\b') { 
                    $messages += "Complex flow logic detected in ${rawPath}: consider creating a diagram via generate-diagram." 
                }
            }
        }
    }
    
    # Process project knowledge base updates
    if ($normalized -match '(^|/)project-knowledge-base/' -or $normalized -match '(^|/)\.agent-artifacts/project-knowledge-base/') {
        $messages += 'Sync nearest index.md and .agent-artifacts/project-knowledge-base/log.md.'
    }
}

$uniqueMessages = $messages | Select-Object -Unique
if ($uniqueMessages) {
    $formattedMsg = "BA Workflow Reminders:`n- " + ($uniqueMessages -join "`n- ")
    [Console]::WriteLine((@{ systemMessage = $formattedMsg } | ConvertTo-Json -Compress))
}
exit 0
