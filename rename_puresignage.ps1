# PowerShell script to rename "PureSignage" to "Pure Signage" across all files
# Excludes binary files, git directory, and this script itself

Write-Host "Starting rename: PureSignage -> Pure Signage" -ForegroundColor Green

# Define patterns to search and replace
$oldName = "PureSignage"
$newName = "Pure Signage"

# Get all text files (excluding binary, git, and specific directories)
$files = Get-ChildItem -Path . -Recurse -File | 
    Where-Object { 
        $_.Extension -match '\.(py|html|md|txt|json|css|js|po|cfg)$' -and
        $_.FullName -notmatch '\\\.git\\' -and
        $_.FullName -notmatch '\\__pycache__\\' -and
        $_.FullName -notmatch '\\\.mo$' -and
        $_.Name -ne 'rename_puresignage.ps1'
    }

$count = 0
$fileCount = 0

foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw -ErrorAction SilentlyContinue
    
    if ($content -and $content -match $oldName) {
        $newContent = $content -replace $oldName, $newName
        Set-Content -Path $file.FullName -Value $newContent -NoNewline
        $fileCount++
        $occurrences = ([regex]::Matches($content, $oldName)).Count
        $count += $occurrences
        Write-Host "Updated: $($file.FullName) ($occurrences occurrences)" -ForegroundColor Yellow
    }
}

Write-Host "`nRename complete!" -ForegroundColor Green
Write-Host "Files modified: $fileCount" -ForegroundColor Cyan
Write-Host "Total replacements: $count" -ForegroundColor Cyan
Write-Host "`nNote: You may need to recompile translations with:" -ForegroundColor Yellow
Write-Host "python -m babel.messages.frontend compile -d translations" -ForegroundColor White
