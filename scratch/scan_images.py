import os, glob, re

public_dir = r'd:\creashiiftads\public'
html_files = glob.glob(os.path.join(public_dir, '*.html')) + glob.glob(os.path.join(public_dir, 'services', '*.html'))

img_sources = set()
external_sources = set()

for f in html_files:
    rel = os.path.relpath(f, public_dir)
    content = open(f, 'r', encoding='utf-8', errors='ignore').read()
    matches = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', content, re.IGNORECASE)
    for src in matches:
        img_sources.add((rel, src))
        if src.startswith('http'):
            external_sources.add(src)

print(f"Total img tags: {len(img_sources)}")
print("External Image Sources:")
for src in sorted(external_sources):
    print("  ", src)
