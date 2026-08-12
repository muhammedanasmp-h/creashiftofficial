import re

index_path = r'd:\creashiiftads\public\index.html'

with open(index_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Trigger typewriter initialization on DOMContentLoaded instead of window.load
old_init_call = """// Defer heavy or non-essential initializations until after the page fully loads
        window.addEventListener('load', () => {
            const initHeavyScripts = () => {
                // Initialize typewriter animations
                initTypewriter('heroHeadline', 0);
                initTypewriter('heroSubtext', 1500); // Staggered delay for subtext"""

new_init_call = """// Initialize LCP Typewriter animations immediately on DOMContentLoaded for zero render delay
        window.addEventListener('DOMContentLoaded', () => {
            initTypewriter('heroHeadline', 0);
            initTypewriter('heroSubtext', 100); // Reduced delay for immediate LCP rendering"""

if old_init_call in content:
    content = content.replace(old_init_call, new_init_call)
    print("Updated initTypewriter timing in index.html")
else:
    # Pattern fallback
    content = re.sub(
        r'initTypewriter\(\'heroSubtext\',\s*1500\)',
        "initTypewriter('heroSubtext', 100)",
        content
    )
    print("Replaced heroSubtext delay in index.html")

# 2. Update CSS for typewriter-char to be immediately visible on first paint before JS character loop
content = content.replace(
    """.typewriter-char {
            display: inline-block;
            opacity: 0;""",
    """.typewriter-char {
            display: inline-block;
            opacity: 1;"""
)

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("LCP Render Delay fix applied successfully!")
