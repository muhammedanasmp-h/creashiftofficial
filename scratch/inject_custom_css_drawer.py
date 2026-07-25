import os
import re

files = [
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
]

customCSS = """
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
        bottom: 16px !important;
        right: 16px !important;
        left: auto !important;
        width: 80% !important;
        max-width: 340px !important;
        height: calc(100dvh - 32px) !important;
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
        display: flex !important;
        flex-direction: column !important;
    }
    #drawer.opacity-100 #drawerBox {
        transform: scale(1) !important;
        opacity: 1 !important;
    }
"""

newPopupHTML = """
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
            <nav class="px-8 py-3 flex-grow flex flex-col justify-center">
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
"""

newToggleJS = """        function toggleDrawer(open) {
            if (open) {
                drawer.classList.add('opacity-100');
                document.body.style.overflow = 'hidden';
            } else {
                drawer.classList.remove('opacity-100');
                document.body.style.overflow = '';
            }
        }"""

for filename in files:
    filepath = os.path.join("d:\\creashiiftads\\public", filename)
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            encoding_used = 'utf-8'
    except UnicodeDecodeError:
        with open(filepath, 'r', encoding='cp1252') as f:
            content = f.read()
            encoding_used = 'cp1252'

    # Remove existing Mobile Navigation Styles block if it exists
    content = re.sub(r'/\* Mobile Navigation Popup Styles \*/.*?(?=\n\s*</style>)', '', content, flags=re.DOTALL)
    
    # Inject CSS
    content = content.replace('</style>', customCSS + '\n</style>', 1)

    # Clean up and replace the HTML popup block
    html_pattern = re.compile(r'<!-- (Mobile Navigation Popup|Hidden Navigation Drawer) -->.*?<div id="drawer".*?</div>\s*</div>\s*</div>\s*(?=<script>)', re.DOTALL)
    if html_pattern.search(content):
        content = html_pattern.sub(newPopupHTML, content)
    else:
        pattern2 = re.compile(r'<div class="h-full w-full fixed inset-0 z-\[60\] bg-white translate-x-full.*?START A PROJECT\s*</(button|a)>\s*</div>\s*</div>\s*</div>', re.DOTALL)
        if pattern2.search(content):
            content = pattern2.sub(newPopupHTML, content)

    # Cleanup double/weird residues
    content = re.sub(r'<!-- Mobile Navigation Popup -->.*?<div id="drawer">.*?</div>\s*</div>\s*</div>\s*<!-- Mobile Navigation Popup -->', newPopupHTML, content, flags=re.DOTALL)

    # Update toggle JS
    toggle_pattern = re.compile(r'function toggleDrawer\(open\)\s*\{.*?\}', re.DOTALL)
    content = toggle_pattern.sub(newToggleJS, content)

    # Clean up redundant drawerBox variable if present
    content = re.sub(r'const drawerBox = document\.getElementById\(\'drawerBox\'\);\s*\n', '', content)
    content = re.sub(r'if\s*\(drawerBox\)\s*\{\s*drawerBox\.classList\..*?\n\s*\}', '', content)
    content = re.sub(r'if\s*\(drawerBox\)\s*drawerBox\.classList\..*?\n', '', content)

    # Clean backdrop tap listener
    content = re.sub(r'// Close on backdrop tap\s*drawer\.addEventListener\(\'click\',.*?\}\);\s*\n', '', content, flags=re.DOTALL)

    # Insert clean backdrop tap listener
    drawer_links_pattern = re.compile(r'(drawerLinks\.forEach\(link\s*=>\s*\{\s*\n?\s*link\.addEventListener\(\'click\',\s*\(\)\s*=>\s*toggleDrawer\(false\)\);\s*\n?\s*\}\);)')
    backdrop_listener = r"""\1

        // Close on backdrop tap
        drawer.addEventListener('click', (e) => {
            if (e.target === drawer || e.target.classList.contains('drawer-backdrop')) {
                toggleDrawer(false);
            }
        });"""
    content = drawer_links_pattern.sub(backdrop_listener, content)

    with open(filepath, 'w', encoding=encoding_used) as f:
        f.write(content)
    print(f"Successfully processed: {filename} ({encoding_used})")
