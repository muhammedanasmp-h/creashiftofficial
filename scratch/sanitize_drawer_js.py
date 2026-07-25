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

cleanJS = """        const menuBtn = document.getElementById('menuBtn');
        const closeDrawer = document.getElementById('closeDrawer');
        const drawer = document.getElementById('drawer');
        const drawerLinks = drawer.querySelectorAll('nav a');

        function toggleDrawer(open) {
            if (open) {
                drawer.classList.add('opacity-100');
                document.body.style.overflow = 'hidden';
            } else {
                drawer.classList.remove('opacity-100');
                document.body.style.overflow = '';
            }
        }

        if (menuBtn) menuBtn.addEventListener('click', () => toggleDrawer(true));
        if (closeDrawer) closeDrawer.addEventListener('click', () => toggleDrawer(false));
        drawerLinks.forEach(link => {
            link.addEventListener('click', () => toggleDrawer(false));
        });

        // Close on backdrop tap
        drawer.addEventListener('click', (e) => {
            if (e.target === drawer || e.target.classList.contains('drawer-backdrop')) {
                toggleDrawer(false);
            }
        });"""

# Match starting with menuBtn/closeDrawer declaration down to the end of the menu click listener block
pattern = re.compile(
    r'(const\s+menuBtn\s*=\s*document\.getElementById\(\'menuBtn\'\);|const\s+closeDrawer\s*=\s*document\.getElementById\(\'closeDrawer\'\);).*?'
    r'(?=\n\s*(//\s*(WhatsApp|Lead|Check|Contact|Form|Close on backdrop)|const\s+contactForm|setTimeout\())', 
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

    if pattern.search(content):
        content = pattern.sub(cleanJS, content)
        with open(filepath, 'w', encoding=encoding_used) as f:
            f.write(content)
        print(f"Successfully sanitized JS: {filename} ({encoding_used})")
    else:
        print(f"ERROR: Could not match pattern in {filename}")
