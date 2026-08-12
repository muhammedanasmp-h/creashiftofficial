import glob, re, os

public_dir = r'd:\creashiiftads\public'
files = glob.glob(os.path.join(public_dir, '*.html')) + glob.glob(os.path.join(public_dir, 'services', '*.html')) + glob.glob(os.path.join(public_dir, 'js', '*.js'))

reflow_patterns = ['offsetWidth', 'offsetHeight', 'getBoundingClientRect', 'scrollTop', 'offsetTop', 'scrollWidth', 'scrollLeft', 'clientHeight', 'clientWidth']

for f in files:
    rel = os.path.relpath(f, public_dir)
    content = open(f, 'r', encoding='utf-8', errors='ignore').read()
    found = []
    for pattern in reflow_patterns:
        count = len(re.findall(re.escape(pattern), content))
        if count > 0:
            found.append(f"{pattern} ({count}x)")
    if found:
        print(f"{rel}: {', '.join(found)}")
