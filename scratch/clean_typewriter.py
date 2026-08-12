import os, re

index_path = r'd:\creashiiftads\public\index.html'
about_path = r'd:\creashiiftads\public\about.html'
contact_path = r'd:\creashiiftads\public\contact.html'

def clean_typewriter(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Replace initTypewriter function with no-op dummy function so any legacy call doesn't break
    dummy_func = "// Instant Native Rendering - Typewriter JS overhead disabled for 95+ LCP\n        function initTypewriter() {}"
    
    pattern = re.compile(r'// Zero-Delay Instant LCP Typewriter Effect\s*function initTypewriter\(elementId\)\s*\{.*?\n\s*\}', re.DOTALL)
    if not pattern.search(content):
        pattern = re.compile(r'// (?:Blurry )?Typewriter Effect.*?\n\s*function initTypewriter\(.*?\)\s*\{.*?\n\s*\}', re.DOTALL)
    
    content = pattern.sub(dummy_func, content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Cleanly disabled initTypewriter in {os.path.basename(file_path)}")

clean_typewriter(index_path)
clean_typewriter(about_path)
clean_typewriter(contact_path)
