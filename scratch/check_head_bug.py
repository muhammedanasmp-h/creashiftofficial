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

for filename in files:
    filepath = os.path.join("d:\\creashiiftads\\public", filename)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(filepath, 'r', encoding='cp1252') as f:
            content = f.read()
            
    # Check if 'id="drawer"' is located before '</head>'
    head_match = re.search(r'</head>', content, re.IGNORECASE)
    if head_match:
        head_index = head_match.start()
        drawer_match = re.search(r'id="drawer"', content)
        if drawer_match and drawer_match.start() < head_index:
            print(f"BUG FOUND: {filename} has the mobile menu popup inside the <head> tag!")
        else:
            print(f"OK: {filename} has the mobile menu popup outside the <head> tag.")
    else:
        print(f"WARNING: No </head> tag found in {filename}")
