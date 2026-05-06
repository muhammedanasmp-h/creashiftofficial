$files = Get-ChildItem -Path "public" -Filter "*.html" -Recurse
$socialTags = @"
    <!-- Social Media Preview (Open Graph) -->
    <meta property="og:title" content="CREASHIFT | Shifting Digital Visions">
    <meta property="og:description" content="Boutique Digital Agency specializing in premium SEO, high-end web engineering, and strategic brand growth.">
    <meta property="og:image" content="https://creashift.com/assets/logo123.png">
    <meta property="og:url" content="https://creashift.com/">
    <meta property="og:type" content="website">
    
    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="CREASHIFT | Shifting Digital Visions">
    <meta name="twitter:description" content="Boutique Digital Agency specializing in premium SEO, high-end web engineering, and strategic brand growth.">
    <meta name="twitter:image" content="https://creashift.com/assets/logo123.png">
"@

foreach ($file in $files) {
    $content = Get-Content -Path $file.FullName -Raw
    if ($content -notlike "*Social Media Preview*") {
        # Insert after the favicon tags we added earlier
        $newContent = $content -replace "(<!-- Favicon / Site Icon -->)", "$socialTags`n`n    `$1"
        Set-Content -Path $file.FullName -Value $newContent
        Write-Host "Added social tags to $($file.Name)"
    }
}
