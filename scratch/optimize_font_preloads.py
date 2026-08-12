import os, glob

public_dir = r'd:\creashiiftads\public'

html_files = glob.glob(os.path.join(public_dir, '*.html')) + glob.glob(os.path.join(public_dir, 'services', '*.html'))

preload_block = """    <link rel="preload" href="/fonts/dm-sans-latin.woff2" as="font" type="font/woff2" crossorigin>
    <link rel="preload" href="/fonts/dm-sans-italic-latin.woff2" as="font" type="font/woff2" crossorigin>
    <link rel="preload" href="/fonts/material-symbols-outlined.woff2" as="font" type="font/woff2" crossorigin>
    <link rel="preload" href="/css/main.min.css" as="style">
    <link rel="stylesheet" href="/css/main.min.css">"""

for file_path in html_files:
    rel_path = os.path.relpath(file_path, public_dir)
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Check if dm-sans-italic-latin.woff2 preload exists
    if 'dm-sans-italic-latin.woff2' not in content:
        # Replace existing dm-sans-latin preload block
        if '<link rel="preload" href="/fonts/dm-sans-latin.woff2"' in content:
            # Find range from first preload to stylesheet line
            old_block_start = content.find('<link rel="preload" href="/fonts/dm-sans-latin.woff2"')
            old_block_end = content.find('<link rel="stylesheet" href="/css/main.min.css">') + len('<link rel="stylesheet" href="/css/main.min.css">')
            if old_block_start != -1 and old_block_end != -1:
                new_content = content[:old_block_start] + preload_block + content[old_block_end:]
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f'Updated font & CSS preloads in {rel_path}')
            else:
                print(f'Could not find exact block markers in {rel_path}')
        else:
            print(f'No dm-sans-latin preload in {rel_path}')
    else:
        print(f'Already has italic font preload in {rel_path}')
