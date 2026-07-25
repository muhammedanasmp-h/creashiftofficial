$files = @(
    'blog-post.html',
    'blog.html',
    'service-ads.html',
    'service-design.html',
    'service-seo.html',
    'service-social.html',
    'service-video.html',
    'service-web.html'
)

foreach ($file in $files) {
    $path = "d:\creashiiftads\public\$file"
    $lines = Get-Content $path
    $newLines = @()
    $skipping = $false
    $braceDepth = 0
    
    for ($i = 0; $i -lt $lines.Count; $i++) {
        $line = $lines[$i]
        
        # Detect start of old drawer
        if ($line -match 'translate-x-full' -and $line -match 'id="drawer"') {
            $skipping = $true
            # Count opening divs to track nesting
            $braceDepth = 1
            continue
        }
        
        if ($skipping) {
            # Count div opens and closes
            $opens = ([regex]::Matches($line, '<div[\s>]')).Count
            $closes = ([regex]::Matches($line, '</div>')).Count
            $braceDepth = $braceDepth + $opens - $closes
            
            if ($braceDepth -le 0) {
                $skipping = $false
            }
            continue
        }
        
        $newLines += $line
    }
    
    $newLines -join "`n" | Set-Content $path -NoNewline
    Write-Host "Cleaned: $file"
}

# Verify
$remaining = Select-String -Path 'd:\creashiiftads\public\*.html' -Pattern 'translate-x-full' -List | Select-Object -ExpandProperty Filename
if ($remaining) {
    Write-Host "`nWARNING: Still found in: $($remaining -join ', ')"
} else {
    Write-Host "`nSUCCESS: All old drawers removed!"
}
