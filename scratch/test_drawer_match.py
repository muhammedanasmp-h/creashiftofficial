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
    except UnicodeDecodeError:
        with open(filepath, 'r', encoding='cp1252') as f:
            content = f.read()
            
    match = drawer_pattern.search(content)
    if match:
        print(f"Matched drawer in {filename}:")
        lines = match.group(0).strip().split('\n')
        print(f"  First line: {lines[0]}")
        print(f"  Last line:  {lines[-1]}")
        print(f"  Total lines: {len(lines)}")
    else:
        print(f"FAILED to match drawer in {filename}")
