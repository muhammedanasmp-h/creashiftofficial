# Creashift Push Script
# Usage: .\push.ps1 "Your commit message"
# Or just: .\push.ps1 (uses "Manual update" as default message)

$message = $args[0]
if (-not $message) {
    $message = "Manual update: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
}

Write-Host "Staging all files..." -ForegroundColor Cyan
git add .

Write-Host "Committing changes with message: '$message'..." -ForegroundColor Green
git commit -m $message

Write-Host "Pushing to GitHub..." -ForegroundColor Cyan
git push

Write-Host "Successfully pushed to GitHub!" -ForegroundColor Yellow
