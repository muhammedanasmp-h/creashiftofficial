import re

index_path = r'd:\creashiiftads\public\index.html'

with open(index_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Clean typewriter-char CSS so text is 100% crisp without blur or translateY
old_char_css = """.typewriter-char {
            display: inline-block;
            opacity: 1;
            filter: blur(10px);
            transform: translateY(5px);
            transition: all 0.6s cubic-bezier(0.25, 0.1, 0.25, 1);
        }"""

new_char_css = """.typewriter-char {
            display: inline-block;
            opacity: 1;
            filter: none;
            transform: none;
        }"""

if old_char_css in content:
    content = content.replace(old_char_css, new_char_css)
    print("Cleaned typewriter-char CSS blur/translateY")

# 2. Add Mobile optimization to pause heavy backdrop-blur keyframes on mobile GPU
mobile_speed_css = """        /* Mobile Speed Index Optimization */
        @media (max-width: 768px) {
            .puzzle-tile {
                animation: none !important;
                backdrop-filter: none !important;
                -webkit-backdrop-filter: none !important;
            }
        }"""

if "/* Mobile Speed Index Optimization */" not in content:
    content = content.replace(
        "/* Mobile Optimization */",
        mobile_speed_css + "\n        /* Mobile Optimization */"
    )
    print("Added Mobile Speed Index GPU optimization")

# 3. Add logo image preload
logo_preload = '<link rel="preload" href="/assets/logo123.png" as="image" type="image/png">'
if logo_preload not in content:
    content = content.replace(
        '<link rel="preload" href="/fonts/dm-sans-latin.woff2"',
        f'{logo_preload}\n    <link rel="preload" href="/fonts/dm-sans-latin.woff2"'
    )
    print("Added logo image preload tag")

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Speed Index optimizations applied successfully!")
