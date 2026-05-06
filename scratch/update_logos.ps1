$files = Get-ChildItem -Path "public" -Filter "*.html" -Recurse
foreach ($file in $files) {
    $content = Get-Content -Path $file.FullName -Raw
    if ($content -like "*assets/logo.png*") {
        $newContent = $content -replace "assets/logo.png", "assets/logo123.png"
        Set-Content -Path $file.FullName -Value $newContent
        Write-Host "Updated $($file.Name)"
    }
}
