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

newPopupHTML = """
    <!-- Mobile Navigation Popup -->
    <div id="drawer">
        <!-- Backdrop -->
        <div class="drawer-backdrop"></div>
        <!-- Popup Box -->
        <div id="drawerBox">
            <!-- Header -->
            <div class="flex justify-between items-center px-8 pt-10 pb-4">
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
            <nav class="px-8 py-2">
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

# Regex to match the drawer block (old or new)
drawer_pattern = re.compile(
    r'<!--\s*(Mobile Navigation Popup|Hidden Navigation Drawer|Navigation Drawer)\s*-->.*?'
    r'<div[^>]*id="drawer"[^>]*>.*?'
    r'</div>\s*</div>',
    re.DOTALL
)

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

    # 1. Delete the existing drawer block
    if drawer_pattern.search(content):
        content = drawer_pattern.sub('', content)
        
        # 2. Find the body tag and insert newPopupHTML right after it
        body_pattern = re.compile(r'<body[^>]*>', re.IGNORECASE)
        body_match = body_pattern.search(content)
        if body_match:
            body_tag = body_match.group(0)
            content = content.replace(body_tag, body_tag + '\n' + newPopupHTML, 1)
            with open(filepath, 'w', encoding=encoding_used) as f:
                f.write(content)
            print(f"Successfully relocated drawer HTML to <body> tag in: {filename}")
        else:
            print(f"ERROR: Could not find <body> tag in {filename}")
    else:
        print(f"ERROR: Could not find drawer block to remove in {filename}")
