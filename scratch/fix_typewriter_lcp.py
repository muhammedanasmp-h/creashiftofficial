import os, re

public_dir = r'd:\creashiiftads\public'
index_path = os.path.join(public_dir, 'index.html')
about_path = os.path.join(public_dir, 'about.html')
contact_path = os.path.join(public_dir, 'contact.html')

optimized_typewriter = r"""// Zero-Delay Instant LCP Typewriter Effect
        function initTypewriter(elementId) {
            const element = document.getElementById(elementId);
            if (!element) return;

            const text = element.textContent.trim().replace(/\s+/g, ' ');
            element.textContent = '';

            const cursor = document.createElement('span');
            cursor.className = 'typewriter-cursor';
            element.appendChild(cursor);

            const words = text.split(/\s+/).filter(w => w.length > 0);
            const fragments = document.createDocumentFragment();

            words.forEach((word, wordIdx) => {
                const wordSpan = document.createElement('span');
                wordSpan.style.whiteSpace = 'nowrap';
                wordSpan.style.display = 'inline-block';

                const chars = word.split('');
                chars.forEach((char) => {
                    const span = document.createElement('span');
                    span.textContent = char;
                    span.className = 'typewriter-char visible';
                    wordSpan.appendChild(span);
                });

                fragments.appendChild(wordSpan);
                if (wordIdx < words.length - 1) {
                    fragments.appendChild(document.createTextNode(' '));
                }
            });

            element.insertBefore(fragments, cursor);

            // Hide cursor after initial render
            setTimeout(() => {
                if (cursor) cursor.style.display = 'none';
            }, 800);
        }"""

typewriter_pattern = re.compile(
    r'// (?:Blurry )?Typewriter Effect.*?(?=// Zero-Reflow|// Scroll Reveal|// Mobile Menu|window\.addEventListener)',
    re.DOTALL
)

for path in [index_path, about_path, contact_path]:
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        if typewriter_pattern.search(content):
            content = typewriter_pattern.sub(lambda m: optimized_typewriter + "\n\n        ", content)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated initTypewriter in {os.path.basename(path)}")

print("Typewriter LCP fix applied successfully!")
