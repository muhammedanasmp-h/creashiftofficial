import os, glob, re, json
from PIL import Image

public_dir = r'd:\creashiiftads\public'
assets_dir = os.path.join(public_dir, 'assets')
clients_dir = os.path.join(assets_dir, 'creative clients')
opt_dir = os.path.join(assets_dir, 'optimized')
team_dir = os.path.join(assets_dir, 'our team')

# Load mappings
url_map = {}
if os.path.exists(os.path.join(opt_dir, 'url_map.json')):
    with open(os.path.join(opt_dir, 'url_map.json')) as f:
        url_map = json.load(f)

logo_map = {}
if os.path.exists(os.path.join(clients_dir, 'logo_density_map.json')):
    with open(os.path.join(clients_dir, 'logo_density_map.json')) as f:
        logo_map = json.load(f)

html_files = glob.glob(os.path.join(public_dir, '*.html')) + glob.glob(os.path.join(public_dir, 'services', '*.html'))

# Logo filename normalization lookup
logo_filename_lookup = {}
for fname, data in logo_map.items():
    logo_filename_lookup[fname] = data
    clean = fname.lower().replace(' ', '_').replace('-', '_')
    logo_filename_lookup[clean] = data

for file_path in html_files:
    rel_path = os.path.relpath(file_path, public_dir)
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    modified = content

    # 1. Replace External Google & Unsplash Image URLs with local WebP
    for ext_url, data in url_map.items():
        local_rel, w, h = data[0], data[1], data[2]
        if ext_url in modified:
            modified = modified.replace(ext_url, local_rel)

    # 2. Replace PNG client logo paths with WebP & responsive srcset/sizes
    for orig_fname, ldata in logo_map.items():
        clean = ldata['clean_name']
        primary_rel = ldata['rel_primary']
        srcset = ldata['srcset']
        w = ldata['width']
        h = ldata['height']
        
        # Replace occurrences in src attributes
        pattern = re.compile(r'src=["\'][^"\']*' + re.escape(orig_fname) + r'["\']', re.IGNORECASE)
        replacement = f'src="{primary_rel}" srcset="{srcset}" sizes="(max-width: 768px) 120px, 240px" width="{w}" height="{h}"'
        modified = pattern.sub(replacement, modified)

    # 3. Replace Team PNG paths with WebP
    team_pngs = {
        'asif  lm,lm.png': ('/assets/our team/asif__lm_lm.webp', 400, 533),
        'fasna-1.png': ('/assets/our team/fasna_1.webp', 400, 533),
        'naseera.png': ('/assets/our team/naseera.webp', 400, 533),
        'Nikhil.png': ('/assets/our team/nikhil.webp', 400, 533),
        'Shalim.png': ('/assets/our team/shalim.webp', 400, 533),
        'shiju ggvk.png': ('/assets/our team/shiju_ggvk.webp', 400, 533)
    }
    for t_fname, t_info in team_pngs.items():
        pattern = re.compile(r'src=["\'][^"\']*' + re.escape(t_fname) + r'["\']', re.IGNORECASE)
        replacement = f'src="{t_info[0]}" width="{t_info[1]}" height="{t_info[2]}"'
        modified = pattern.sub(replacement, modified)

    # 4. Replace background PNGs
    modified = modified.replace('hero_bg.png', 'hero_bg.webp')
    modified = modified.replace('design-bg.png', 'design-bg.webp')
    modified = modified.replace('video-bg.png', 'video-bg.webp')

    # 5. Add loading, decoding, fetchpriority to all <img> tags if missing
    def update_img_tag(match):
        tag = match.group(0)
        
        # Check if Hero / LCP logo image
        is_hero_logo = 'logo123' in tag or 'CREASHIFT Logo' in tag or 'CREASHIFT Icon' in tag
        
        # Add decoding="async"
        if 'decoding=' not in tag:
            tag = tag[:-1] + ' decoding="async">'
            
        # Add loading & fetchpriority
        if is_hero_logo:
            if 'loading=' not in tag:
                tag = tag[:-1] + ' loading="eager">'
            if 'fetchpriority=' not in tag:
                tag = tag[:-1] + ' fetchpriority="high">'
        else:
            if 'loading=' not in tag:
                tag = tag[:-1] + ' loading="lazy">'
            if 'fetchpriority=' not in tag:
                tag = tag[:-1] + ' fetchpriority="low">'
                
        # Ensure width and height exist
        if 'width=' not in tag and ('logo123' in tag or 'CREASHIFT' in tag):
            tag = tag[:-1] + ' width="28" height="28">'
            
        return tag

    modified = re.sub(r'<img[^>]+>', update_img_tag, modified)

    if modified != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(modified)
        print(f"Updated HTML image tags in {rel_path}")
    else:
        print(f"No changes needed for {rel_path}")

print("HTML Image Tag update complete!")
