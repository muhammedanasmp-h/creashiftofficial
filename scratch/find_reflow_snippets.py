import glob, re, os

public_dir = r'd:\creashiiftads\public'
files = glob.glob(os.path.join(public_dir, '*.html')) + glob.glob(os.path.join(public_dir, 'services', '*.html'))

reflow_patterns = ['offsetWidth', 'offsetHeight', 'getBoundingClientRect', 'scrollTop', 'offsetTop', 'scrollWidth', 'scrollLeft', 'clientHeight', 'clientWidth', 'setInterval', 'scroll']

for f in files:
    rel = os.path.relpath(f, public_dir)
    lines = open(f, 'r', encoding='utf-8', errors='ignore').readlines()
    for idx, line in enumerate(lines, 1):
        for pattern in reflow_patterns:
            if pattern in line and ('<script' in line or idx > 100):
                print(f"{rel}:{idx} [{pattern}] => {line.strip()[:100]}")
