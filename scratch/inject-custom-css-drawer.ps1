$files = @(
    'about.html',
    'blog-post.html',
    'blog.html',
    'contact.html',
    'index.html',
    'portfolio.html',
    'service-ads.html',
    'service-design.html',
    'service-seo.html',
    'service-social.html',
    'service-video.html',
    'service-web.html',
    'services.html'
)

$customCSS = @'
    /* Mobile Navigation Popup Styles */
    #drawer {
        position: fixed !important;
        inset: 0 !important;
        z-index: 99999 !important;
        opacity: 0;
        visibility: hidden;
        pointer-events: none;
        transition: opacity 0.4s ease, visibility 0.4s ease;
    }
    #drawer.opacity-100 {
        opacity: 1 !important;
        visibility: visible !important;
        pointer-events: auto !important;
    }
    .drawer-backdrop {
        position: absolute !important;
        inset: 0 !important;
        background: rgba(0, 0, 0, 0.3) !important;
        backdrop-filter: blur(4px) !important;
        -webkit-backdrop-filter: blur(4px) !important;
    }
    #drawerBox {
        position: absolute !important;
        top: 16px !important;
        right: 16px !important;
        left: auto !important;
        bottom: auto !important;
        width: 78% !important;
        max-width: 320px !important;
        background: #ffffff !important;
        border-radius: 28px !important;
        transform-origin: top right !important;
        transform: scale(0.3) !important;
        opacity: 0 !important;
        transition: transform 0.4s cubic-bezier(0.32, 0.72, 0, 1), opacity 0.4s ease !important;
        box-shadow: 0 20px 60px -10px rgba(0, 0, 0, 0.25) !important;
        border: 1px solid rgba(0, 0, 0, 0.05) !important;
        overflow: hidden !important;
        z-index: 100000 !important;
    }
    #drawer.opacity-100 #drawerBox {
        transform: scale(1) !important;
        opacity: 1 !important;
    }
'@

$newPopupHTML = @'
    <!-- Mobile Navigation Popup -->
    <div id="drawer">
        <!-- Backdrop -->
        <div class="drawer-backdrop"></div>
        <!-- Popup Box -->
        <div id="drawerBox">
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
    
    # 1. Inject the custom CSS rules into the first style block (right before </style>)
    if ($content -notmatch 'Mobile Navigation Popup Styles') {
        $rxCSS = [regex]::new('</style>')
        $content = $rxCSS.Replace($content, ($customCSS + "`n</style>"), 1)
    }
    
    # 2. Replace the HTML block starting with <!-- Mobile Navigation Popup --> or <!-- Hidden Navigation Drawer --> up to the next script tag
    $rxHTML = [regex]::new('(?s)<!-- (Mobile Navigation Popup|Hidden Navigation Drawer) -->.*?<div id="drawer".*?</div>\s*</div>\s*</div>\s*(?=<script>)')
    if ($content -match 'Mobile Navigation Popup') {
        $content = $rxHTML.Replace($content, $newPopupHTML, 1)
    } else {
        # If the tag is not already formatted, clean it using regex from previous script or clean it first
        $pattern = '(?s)<div class="h-full w-full fixed inset-0 z-\[60\] bg-white translate-x-full.*?START A PROJECT\s*</(button|a)>\s*</div>\s*</div>\s*</div>'
        $content = [regex]::Replace($content, $pattern, $newPopupHTML.Trim())
    }
    
    # Let's verify that the HTML block is clean
    $content = $content -replace '(?s)<!-- Mobile Navigation Popup -->.*?<div id="drawer">.*?</div>\s*</div>\s*</div>\s*<!-- Mobile Navigation Popup -->', $newPopupHTML
    
    # 3. Clean JS: Re-write the toggleDrawer function and event listeners
    # Locate toggleDrawer function
    $togglePattern = '(?s)function toggleDrawer\(open\)\s*\{.*?\}'
    $newToggleJS = @'
        function toggleDrawer(open) {
            if (open) {
                drawer.classList.add('opacity-100');
                document.body.style.overflow = 'hidden';
            } else {
                drawer.classList.remove('opacity-100');
                document.body.style.overflow = '';
            }
        }
'@
    $content = [regex]::Replace($content, $togglePattern, $newToggleJS.Trim())
    
    # Remove unused drawerBox references in JS if they exist
    $content = $content -replace 'const drawerBox = document\.getElementById\(\''drawerBox\''\);\s*\r?\n', ''
    $content = $content -replace 'if\s*\(drawerBox\)\s*\{\s*drawerBox\.classList\..*?\r?\n\s*\}', ''
    $content = $content -replace 'if\s*\(drawerBox\)\s*drawerBox\.classList\..*?\r?\n', ''
    
    # Clean backdrop close listener to make it completely correct
    if ($content -match 'Close on backdrop tap') {
        # Replace the existing backdrop listener block
        $backdropPattern = '(?s)// Close on backdrop tap\s*drawer\.addEventListener\(\''click\'\+,\s*\(e\)\s*=>\s*\{.*?\}\);'
        $content = [regex]::Replace($content, $backdropPattern, '')
    }
    
    # Ensure backdrop listener is added once cleanly
    $content = $content -replace '(?s)// Close on backdrop tap\s*drawer\.addEventListener\(\''click\'\',\s*\(e\)\s*=>\s*\{.*?\}\);', ''
    
    # Find the drawerLinks block and append/replace backdrop tap listener
    $drawerLinksPattern = '(?s)(drawerLinks\.forEach\(link\s*=>\s*\{\s*\r?\n?\s*link\.addEventListener\(\''click\'\',\s*\(\)\s*=>\s*toggleDrawer\(false\)\);\s*\r?\n?\s*\}\);)'
    $backdropListener = @'
$1
        // Close on backdrop tap
        drawer.addEventListener('click', (e) => {
            if (e.target === drawer || e.target.classList.contains('drawer-backdrop')) {
                toggleDrawer(false);
            }
        });
'@
    # Clean any duplicates of this listener
    $content = $content -replace '(?s)// Close on backdrop tap.*?toggleDrawer\(false\);\s*\}\s*\);\s*', ''
    $content = [regex]::Replace($content, $drawerLinksPattern, $backdropListener)
    
    Set-Content $path $content -NoNewline
    Write-Host "Updated page style & drawer: $file"
}
