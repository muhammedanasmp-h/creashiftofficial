import os, glob, re, urllib.request

public_dir = r'd:\creashiiftads\public'
html_files = glob.glob(os.path.join(public_dir, '*.html')) + glob.glob(os.path.join(public_dir, 'services', '*.html'))

google_imgs = []

for f in html_files:
    rel = os.path.relpath(f, public_dir)
    content = open(f, 'r', encoding='utf-8', errors='ignore').read()
    matches = re.findall(r'(https://lh3\.googleusercontent\.com/aida-public/[^\s"\'<>]+)', content)
    for url in matches:
        google_imgs.append((rel, url))

print(f"Found {len(google_imgs)} references to Google images:")
for rel, url in google_imgs:
    print(f"File: {rel}")
    print(f"  URL: {url[:80]}...")
