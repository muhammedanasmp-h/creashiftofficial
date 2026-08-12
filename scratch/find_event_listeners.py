import glob, re, os

public_dir = r'd:\creashiiftads\public'
files = glob.glob(os.path.join(public_dir, '*.html')) + glob.glob(os.path.join(public_dir, 'services', '*.html'))

for f in files:
    rel = os.path.relpath(f, public_dir)
    content = open(f, 'r', encoding='utf-8', errors='ignore').read()
    if 'mousemove' in content or 'scroll' in content:
        lines = content.split('\n')
        for idx, line in enumerate(lines, 1):
            if ('mousemove' in line or 'addEventListener(\'scroll\'' in line or 'addEventListener("scroll"' in line) and '<style' not in line:
                print(f"{rel}:{idx} => {line.strip()[:100]}")
