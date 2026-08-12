import glob, re, os

public_dir = r'd:\creashiiftads\public'
files = glob.glob(os.path.join(public_dir, '*.html')) + glob.glob(os.path.join(public_dir, 'services', '*.html'))

gtag_script_block = """<!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-FK6M5T8E3J"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-FK6M5T8E3J');
    </script>"""

# Pattern to match gtag block anywhere
gtag_regex = re.compile(
    r'<!-- Google tag \(gtag\.js\) -->\s*<script async src="https://www\.googletagmanager\.com/gtag/js\?id=G-FK6M5T8E3J"></script>\s*<script>\s*window\.dataLayer = window\.dataLayer \|\| \[\];\s*function gtag\(\)\{dataLayer\.push\(arguments\);\}\s*gtag\(\'js\', new Date\(\)\);\s*gtag\(\'config\', \'G-FK6M5T8E3J\'\);\s*</script>',
    re.MULTILINE
)

updated_count = 0

for f in files:
    rel = os.path.relpath(f, public_dir)
    content = open(f, 'r', encoding='utf-8', errors='ignore').read()
    
    # 1. Remove ALL existing gtag blocks from content
    clean_content = gtag_regex.sub('', content)
    
    # 2. Insert ONE non-blocking gtag block right before </head>
    if '</head>' in clean_content:
        # Load gtag asynchronously before </head>
        deferred_gtag = f"""    {gtag_script_block}
</head>"""
        new_content = clean_content.replace('</head>', deferred_gtag, 1)
        with open(f, 'w', encoding='utf-8') as out:
            out.write(new_content)
        updated_count += 1
        print(f"Optimized GTag loading in {rel}")

print(f"Successfully optimized GTag script loading in {updated_count} files!")
