$files = @(
    'blog-post.html',
    'blog.html',
    'portfolio.html',
    'service-ads.html',
    'service-design.html',
    'service-seo.html',
    'service-social.html',
    'service-video.html',
    'service-web.html'
)

$newPopup = @'
    <!-- Mobile Navigation Popup -->
    <div class="fixed inset-0 z-[60] opacity-0 invisible pointer-events-none transition-all duration-400" id="drawer">
        <!-- Backdrop -->
        <div class="absolute inset-0 bg-black/30 backdrop-blur-sm"></div>
        <!-- Popup Box -->
        <div class="absolute top-[12px] right-[12px] w-[78%] max-w-[320px] bg-white rounded-[28px] shadow-[0_20px_60px_-10px_rgba(0,0,0,0.25)] border border-black/5 overflow-hidden origin-top-right scale-[0.3] opacity-0 transition-all duration-400 ease-[cubic-bezier(0.32,0.72,0,1)]" id="drawerBox">
            <!-- Header -->
            <div class="flex justify-between items-center px-8 pt-7 pb-4">
                <div class="flex items-center gap-2.5">
                    <div class="h-7 w-7 overflow-hidden flex-shrink-0">
                        <img src="/assets/logo123.png?v=2" alt="CREASHIFT Logo" class="h-full w-auto max-w-none object-cover object-left">
                    </div>
                    <span class="text-base font-black tracking-tighter text-black uppercase">CREASHIFT</span>
                </div>
                <button class="w-10 h-10 flex items-center justify-center rounded-full bg-black/5 hover:bg-black/10 transition-colors" id="closeDrawer" aria-label="Close menu">
                    <span class="material-symbols-outlined text-xl">close</span>
                </button>
            </div>
            <!-- Nav Links -->
            <nav class="px-8 py-3">
                <a class="group flex items-center justify-between py-4 border-b border-black/5" href="/">
                    <span class="text-[15px] font-bold uppercase tracking-[0.12em] text-black">Home</span>
                    <span class="material-symbols-outlined text-black/15 text-lg group-hover:text-black transition-colors">arrow_outward</span>
                </a>
                <a class="group flex items-center justify-between py-4 border-b border-black/5" href="/about">
                    <span class="text-[15px] font-bold uppercase tracking-[0.12em] text-black">About</span>
                    <span class="material-symbols-outlined text-black/15 text-lg group-hover:text-black transition-colors">arrow_outward</span>
                </a>
                <a class="group flex items-center justify-between py-4 border-b border-black/5" href="/services">
                    <span class="text-[15px] font-bold uppercase tracking-[0.12em] text-black">Services</span>
                    <span class="material-symbols-outlined text-black/15 text-lg group-hover:text-black transition-colors">arrow_outward</span>
                </a>
                <a class="group flex items-center justify-between py-4 border-b border-black/5" href="/portfolio">
                    <span class="text-[15px] font-bold uppercase tracking-[0.12em] text-black">Portfolio</span>
                    <span class="material-symbols-outlined text-black/15 text-lg group-hover:text-black transition-colors">arrow_outward</span>
                </a>
                <a class="group flex items-center justify-between py-4 border-b border-black/5" href="/blog">
                    <span class="text-[15px] font-bold uppercase tracking-[0.12em] text-black">Blog</span>
                    <span class="material-symbols-outlined text-black/15 text-lg group-hover:text-black transition-colors">arrow_outward</span>
                </a>
                <a class="group flex items-center justify-between py-4" href="/contact">
                    <span class="text-[15px] font-bold uppercase tracking-[0.12em] text-black">Contact</span>
                    <span class="material-symbols-outlined text-black/15 text-lg group-hover:text-black transition-colors">arrow_outward</span>
                </a>
            </nav>
            <!-- Bottom CTA -->
            <div class="px-8 pb-7 pt-3">
                <a href="/contact" class="block w-full bg-black text-white text-center font-bold text-[12px] uppercase tracking-[0.2em] py-4.5 rounded-2xl hover:bg-zinc-800 transition-colors">
                    Start a Project
                </a>
                <div class="flex items-center justify-center gap-6 mt-5">
                    <a href="https://www.instagram.com/creashiftads" target="_blank" class="text-[10px] uppercase tracking-[0.2em] text-black/30 hover:text-black transition-colors">Instagram</a>
                    <span class="w-1 h-1 rounded-full bg-black/10"></span>
                    <a href="https://www.linkedin.com/company/creashift/" target="_blank" class="text-[10px] uppercase tracking-[0.2em] text-black/30 hover:text-black transition-colors">LinkedIn</a>
                    <span class="w-1 h-1 rounded-full bg-black/10"></span>
                    <a href="https://wa.me/918086180780" target="_blank" class="text-[10px] uppercase tracking-[0.2em] text-black/30 hover:text-black transition-colors">WhatsApp</a>
                </div>
            </div>
        </div>
    </div>
'@

foreach ($file in $files) {
    $path = "d:\creashiiftads\public\$file"
    $content = Get-Content $path -Raw
    
    # Replace old drawer: match from the opening div with translate-x-full to the matching closing structure
    $pattern = '(?s)<div class="h-full w-full fixed inset-0 z-\[60\] bg-white translate-x-full.*?START A PROJECT\s*</(button|a)>\s*</div>\s*</div>\s*</div>'
    $content = [regex]::Replace($content, $pattern, $newPopup.Trim())
    
    # Replace old toggle function
    $oldToggle = "(?s)function toggleDrawer\(open\) \{\s*if \(open\) \{\s*drawer\.classList\.remove\('translate-x-full',\s*'invisible',\s*'pointer-events-none'\);\s*document\.body\.style\.overflow = 'hidden';\s*\} else \{\s*drawer\.classList\.add\('translate-x-full',\s*'invisible',\s*'pointer-events-none'\);\s*document\.body\.style\.overflow = '';\s*\}\s*\}"
    $newToggle = @"
        function toggleDrawer(open) {
            if (open) {
                drawer.classList.remove('opacity-0', 'invisible', 'pointer-events-none');
                drawer.classList.add('opacity-100');
                if (drawerBox) {
                    drawerBox.classList.remove('scale-[0.3]', 'opacity-0');
                    drawerBox.classList.add('scale-100', 'opacity-100');
                }
                document.body.style.overflow = 'hidden';
            } else {
                drawer.classList.add('opacity-0', 'invisible', 'pointer-events-none');
                drawer.classList.remove('opacity-100');
                if (drawerBox) {
                    drawerBox.classList.add('scale-[0.3]', 'opacity-0');
                    drawerBox.classList.remove('scale-100', 'opacity-100');
                }
                document.body.style.overflow = '';
            }
        }
"@
    $content = [regex]::Replace($content, $oldToggle, $newToggle)
    
    # Add drawerBox variable if not present
    if ($content -notmatch "drawerBox") {
        $content = $content -replace "(const drawer = document\.getElementById\('drawer'\);)", "`$1`n        const drawerBox = document.getElementById('drawerBox');"
    }
    
    # Add backdrop close if not present
    if ($content -notmatch 'Close on backdrop tap') {
        $content = $content -replace "(drawerLinks\.forEach\(link\s*=>\s*\{\s*link\.addEventListener\('click',\s*\(\)\s*=>\s*toggleDrawer\(false\)\);\s*\}\);)", @"
`$1
        // Close on backdrop tap
        drawer.addEventListener('click', (e) => {
            if (e.target === drawer || e.target.classList.contains('backdrop-blur-sm')) {
                toggleDrawer(false);
            }
        });
"@
    }
    
    Set-Content $path $content -NoNewline
    Write-Host "Updated: $file"
}

Write-Host "`nDone! Verifying no old drawers remain..."
$remaining = Select-String -Path 'd:\creashiiftads\public\*.html' -Pattern 'translate-x-full' -List | Select-Object -ExpandProperty Filename
if ($remaining) {
    Write-Host "WARNING: Old drawer still found in: $($remaining -join ', ')"
} else {
    Write-Host "SUCCESS: All old drawers replaced!"
}
