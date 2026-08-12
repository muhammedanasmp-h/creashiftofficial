import os
import glob
import re

html_files = glob.glob("d:/creashiiftads/public/**/*.html", recursive=True)

old_pattern = re.compile(
    r'const navEntries = performance\.getEntriesByType\("navigation"\);\s*'
    r'const isRefresh = navEntries\.length > 0 && navEntries\[0\]\.type === \'reload\';\s*'
    r'const isInternalNav = document\.referrer && document\.referrer\.includes\(window\.location\.host\);\s*'
    r'if \(isRefresh \|\| !isInternalNav\) \{\s*'
    r'popup\.classList\.add\(\'active\'\);\s*'
    r'\}',
    re.MULTILINE
)

replacement = """const isClosed = sessionStorage.getItem('creashift_lead_closed');
                    if (!isClosed) {
                        popup.classList.add('active');
                    }"""

modified_count = 0
for fpath in html_files:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if old_pattern.search(content):
        new_content = old_pattern.sub(replacement, content)
        # Also ensure closing sets sessionStorage
        new_content = new_content.replace(
            "popup.classList.remove('active');",
            "popup.classList.remove('active');\n                    sessionStorage.setItem('creashift_lead_closed', 'true');"
        )
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        modified_count += 1
        print(f"Updated: {fpath}")

print(f"Total HTML files updated: {modified_count}")
