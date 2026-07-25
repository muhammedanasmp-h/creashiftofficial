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

# Regex to match from menuBtn down to the start of next block
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
    except UnicodeDecodeError:
        with open(filepath, 'r', encoding='cp1252') as f:
            content = f.read()
            
    match = pattern.search(content)
    if match:
        print(f"Matched in {filename}:")
        lines = match.group(0).strip().split('\n')
        print(f"  First line: {lines[0]}")
        print(f"  Last line:  {lines[-1]}")
        print(f"  Total lines: {len(lines)}")
    else:
        print(f"FAILED to match in {filename}")
