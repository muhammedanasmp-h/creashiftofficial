import os, re

public_dir = r'd:\creashiiftads\public'
index_path = os.path.join(public_dir, 'index.html')
about_path = os.path.join(public_dir, 'about.html')
contact_path = os.path.join(public_dir, 'contact.html')

# 1. Remove initTypewriter function and calls from index.html
with open(index_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove initTypewriter function definition
content = re.sub(r'// Zero-Delay Instant LCP Typewriter Effect\s*function initTypewriter\(elementId\)\s*\{.*?\n\s*\}', '', content, flags=re.DOTALL)
content = re.sub(r'initTypewriter\([^\)]+\);?', '', content)

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Removed typewriter overhead from index.html")

# 2. Remove initTypewriter from about.html
with open(about_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(r'// Zero-Delay Instant LCP Typewriter Effect\s*function initTypewriter\(elementId\)\s*\{.*?\n\s*\}', '', content, flags=re.DOTALL)
content = re.sub(r'initTypewriter\([^\)]+\);?', '', content)

with open(about_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Removed typewriter overhead from about.html")

# 3. Remove initTypewriter from contact.html
with open(contact_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(r'// Zero-Delay Instant LCP Typewriter Effect\s*function initTypewriter\(elementId\)\s*\{.*?\n\s*\}', '', content, flags=re.DOTALL)
content = re.sub(r'initTypewriter\([^\)]+\);?', '', content)

with open(contact_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Removed typewriter overhead from contact.html")

print("All typewriter JS DOM overhead removed successfully!")
