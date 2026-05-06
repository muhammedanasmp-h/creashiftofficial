$files = Get-ChildItem -Path "public" -Filter "*.html" -Recurse
$faviconTags = @"
    <!-- Favicon / Site Icon -->
    <link rel="icon" type="image/png" href="assets/logo123.png">
    <link rel="apple-touch-icon" href="assets/logo123.png">
    <link rel="shortcut icon" href="assets/logo123.png">
"@

foreach ($file in $files) {
    $content = Get-Content -Path $file.FullName -Raw
    if ($content -notlike "*Favicon / Site Icon*") {
        # Insert after <title> tag
        $newContent = $content -replace "(<title>.*</title>)", "`$1`n$faviconTags"
        Set-Content -Path $file.FullName -Value $newContent
        Write-Host "Added favicon to $($file.Name)"
    }
}
