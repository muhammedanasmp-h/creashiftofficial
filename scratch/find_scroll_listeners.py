import glob, re, os

public_dir = r'd:\creashiiftads\public'
files = glob.glob(os.path.join(public_dir, '*.html')) + glob.glob(os.path.join(public_dir, 'services', '*.html'))

for f in files:
    rel = os.path.relpath(f, public_dir)
    lines = open(f, 'r', encoding='utf-8', errors='ignore').readlines()
    for idx, line in enumerate(lines, 1):
        if 'addEventListener(\'scroll\'' in line or 'addEventListener("scroll"' in line or 'window.onscroll' in line or 'window.innerWidth' in line:
            print(f"{rel}:{idx} => {line.strip()[:100]}")
