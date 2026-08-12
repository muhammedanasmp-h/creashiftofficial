import os, glob, sys, urllib.request, json, socket
from PIL import Image

socket.setdefaulttimeout(5)

public_dir = r'd:\creashiiftads\public'
assets_dir = os.path.join(public_dir, 'assets')
opt_dir = os.path.join(assets_dir, 'optimized')
os.makedirs(opt_dir, exist_ok=True)

log_data = []

def print_log(msg):
    print(msg)
    sys.stdout.flush()

def save_webp(img, out_path, max_width=None, quality=82):
    im = img.copy()
    if max_width and im.width > max_width:
        ratio = max_width / float(im.width)
        new_height = int(float(im.height) * ratio)
        im = im.resize((max_width, new_height), Image.Resampling.LANCZOS)
    
    im.save(out_path, 'WEBP', quality=quality, method=6)
    return im.width, im.height, os.path.getsize(out_path)

# 1. Localize External Google & Unsplash Images
print_log("--- 1. Localizing External Images ---")
ext_urls = [
    "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&q=80&w=800",
    "https://images.unsplash.com/photo-1492691527719-9d1e07e534b4?auto=format&fit=crop&q=80&w=800",
    "https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&q=80&w=1200",
    "https://images.unsplash.com/photo-1558655146-d09347e92766?auto=format&fit=crop&q=80&w=800",
    "https://images.unsplash.com/photo-1611162617474-5b21e879e113?auto=format&fit=crop&q=80&w=800",
    "https://lh3.googleusercontent.com/aida-public/AB6AXuAbaajVWq7ldfWKpD35uQayifZNIe2RdLzsLdSdILecue3VgxKfiHfjiH6RVZ2rF-UaOWpvuRl7wnpe9dVlSL2EYykJLocb1hCyvlN55g9H0dp0eDdFj1GynNHAxqVVTAGgVu_HdRFJ6nAzZywML2e8KzdQrqhQSpi8YuL2UmSLWMbRexuI5I4-fzq9qJqivKkZ8kqyM4VzA3opmZULF2Fyfg9RYQE1fVu4bWB5PBi5UnfuoPoIoRvlOelnTu8FEPEFJtdyOnp2fBkK",
    "https://lh3.googleusercontent.com/aida-public/AB6AXuD40GIf4n79O5FYTcBaj0Pog32YohJY-yX9_teRWZPr-HIJkS6g-PEgxgyc5ltR50ogoEItUTZtAlH6d2iDpQbFjNR9n9DU7PHRNJ3yL66HcrLt5EqwgtQj4TOL1WbqlYTrwzcy_FNphXqJM4RlR1UF9t5pwr0Zr9BrIT_mSl9e9mVImXJGMttClS8Yt1GfQz1BxJdQhhA8CgshjP_YKLNKQes5U6PevGSmes-vLu8_8TmmPYIhgA118B2RnP8jn6P-70UX9e8tQQ-x",
    "https://lh3.googleusercontent.com/aida-public/AB6AXuDBAovw4N08jYJmH9q7q-G-95Hj9u6Wn2Sshn8tA5yO5k4O5k4O5k4O5k4O5k4O5k4O5k4O5k4O5k4O5k4O5k4O5k4O",
    "https://lh3.googleusercontent.com/aida-public/AB6AXuDOQRs4hTFRvACoLskIaJUZv8BB-flDqWLXFo-F1PVxdUgmdzdQiFmjXHyu8_IwMBJzXqm232HwxQlPCWJRAaMr9Zb6YwfV0RFWCcJ6z4upul9PyTA1EZbUZd2GbYHyo0M4fbgTBAnhdGv0OLMpZ3QZYHUcQhfWjK406eLmUKaid33UyP70d_u7T1VZcPCJKVzQkR1U04q6XaehJ4ItPBcxN6E3vCo1sNiJan9g4W-uJM79SorlPOMVaroLfL6ui2wN2so4XQMC38lt",
    "https://lh3.googleusercontent.com/aida-public/AB6AXuDR3iwS2RMos8F3Tqtvchp32NR6xc98ihMs5O0UTf5uS6RgT1tvHl3p6xPjAN8nFhFdIlL4wLRAJP_Bd7z6NLoUxt_g9wHnKfL39gqkcEY4aSp-MlgUR2tmnCySu5WC2VuTbBnjoq_XEj_tS2mXHqNjr_AyZr_uMbVpffwBeU4sGrEAuZ1UB2oJRYFb-D_S3fr2WdFbRjsd7wwW4xPorh7ovfZULAhPOHZKRJTB18HNqYk5wzspuI3hQmBWPARR10n_UhiWk4CH_7A_"
]

url_map = {}
for i, url in enumerate(ext_urls, 1):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        temp_file = os.path.join(opt_dir, f'temp_ext_{i}.tmp')
        with urllib.request.urlopen(req, timeout=4) as resp, open(temp_file, 'wb') as f:
            f.write(resp.read())
        
        orig_size = os.path.getsize(temp_file)
        img = Image.open(temp_file)
        out_name = f'ext_{i}.webp'
        out_path = os.path.join(opt_dir, out_name)
        w, h, new_size = save_webp(img, out_path, max_width=800, quality=80)
        if os.path.exists(temp_file):
            os.remove(temp_file)
        
        rel_url = f'/assets/optimized/{out_name}'
        url_map[url] = (rel_url, w, h)
        log_data.append({
            'name': f'External Image #{i}',
            'original_size': orig_size,
            'new_size': new_size,
            'path': rel_url,
            'width': w,
            'height': h
        })
        print_log(f"Downloaded & Optimized External Image #{i}: {orig_size/1024:.1f} KB -> {new_size/1024:.1f} KB ({w}x{h})")
    except Exception as e:
        print_log(f"Failed to fetch external #{i} ({url[:40]}...): {e}")

with open(os.path.join(opt_dir, 'url_map.json'), 'w') as f:
    json.dump(url_map, f, indent=2)

# 2. Process Client Logos
print_log("\n--- 2. Processing Creative Client Logos ---")
clients_dir = os.path.join(assets_dir, 'creative clients')
logo_files = glob.glob(os.path.join(clients_dir, '*.png')) + glob.glob(os.path.join(clients_dir, '*.jpg'))

logo_density_map = {}

for logo_path in logo_files:
    fname = os.path.basename(logo_path)
    if fname.endswith('-120.webp') or fname.endswith('-240.webp') or fname.endswith('-480.webp') or fname.endswith('.webp'):
        continue
    base_name = os.path.splitext(fname)[0].strip()
    orig_size = os.path.getsize(logo_path)
    
    img = Image.open(logo_path)
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    clean_name = base_name.lower().replace(' ', '_').replace('-', '_').replace('(', '').replace(')', '')
    primary_webp = os.path.join(clients_dir, f"{clean_name}.webp")
    pw, ph, psize = save_webp(img, primary_webp, max_width=300, quality=82)
    
    v120 = os.path.join(clients_dir, f"{clean_name}-120.webp")
    w120, h120, s120 = save_webp(img, v120, max_width=120, quality=80)
    
    v240 = os.path.join(clients_dir, f"{clean_name}-240.webp")
    w240, h240, s240 = save_webp(img, v240, max_width=240, quality=82)
    
    v480 = os.path.join(clients_dir, f"{clean_name}-480.webp")
    w480, h480, s480 = save_webp(img, v480, max_width=480, quality=85)
    
    logo_density_map[fname] = {
        'clean_name': clean_name,
        'rel_primary': f"/assets/creative clients/{clean_name}.webp",
        'srcset': f"/assets/creative clients/{clean_name}-120.webp 120w, /assets/creative clients/{clean_name}-240.webp 240w, /assets/creative clients/{clean_name}-480.webp 480w",
        'width': pw,
        'height': ph,
        'aspect_ratio': pw / float(ph)
    }
    
    log_data.append({
        'name': f'Logo: {fname}',
        'original_size': orig_size,
        'new_size': psize,
        'path': f"/assets/creative clients/{clean_name}.webp",
        'width': pw,
        'height': ph
    })
    print_log(f"Optimized Logo {fname}: {orig_size/1024:.1f} KB -> {psize/1024:.1f} KB ({pw}x{ph})")

with open(os.path.join(clients_dir, 'logo_density_map.json'), 'w') as f:
    json.dump(logo_density_map, f, indent=2)

# 3. Process Team Photos
print_log("\n--- 3. Processing Our Team Photos ---")
team_dir = os.path.join(assets_dir, 'our team')
team_files = glob.glob(os.path.join(team_dir, '*.png')) + glob.glob(os.path.join(team_dir, '*.jpg'))

for tpath in team_files:
    fname = os.path.basename(tpath)
    if fname.endswith('.webp'):
        continue
    base_name = os.path.splitext(fname)[0].strip()
    orig_size = os.path.getsize(tpath)
    
    img = Image.open(tpath)
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    clean_name = base_name.lower().replace(' ', '_').replace(',', '_')
    out_webp = os.path.join(team_dir, f"{clean_name}.webp")
    tw, th, tsize = save_webp(img, out_webp, max_width=400, quality=82)
    
    log_data.append({
        'name': f'Team: {fname}',
        'original_size': orig_size,
        'new_size': tsize,
        'path': f"/assets/our team/{clean_name}.webp",
        'width': tw,
        'height': th
    })
    print_log(f"Optimized Team Photo {fname}: {orig_size/1024:.1f} KB -> {tsize/1024:.1f} KB ({tw}x{th})")

# 4. Process Large Background Images
print_log("\n--- 4. Processing Background & Hero Images ---")
large_imgs = [
    (os.path.join(assets_dir, 'hero_bg.png'), '/assets/hero_bg.webp', 1600),
    (os.path.join(assets_dir, 'services', 'design-bg.png'), '/assets/services/design-bg.webp', 1200),
    (os.path.join(assets_dir, 'services', 'video-bg.png'), '/assets/services/video-bg.webp', 1200)
]

for orig_path, rel_out, max_w in large_imgs:
    if os.path.exists(orig_path):
        orig_size = os.path.getsize(orig_path)
        img = Image.open(orig_path)
        if img.mode in ('RGBA', 'LA'):
            img = img.convert('RGBA')
        else:
            img = img.convert('RGB')
        
        full_out = os.path.join(public_dir, rel_out.lstrip('/').replace('/', os.sep))
        os.makedirs(os.path.dirname(full_out), exist_ok=True)
        bw, bh, bsize = save_webp(img, full_out, max_width=max_w, quality=80)
        
        log_data.append({
            'name': f'Background: {os.path.basename(orig_path)}',
            'original_size': orig_size,
            'new_size': bsize,
            'path': rel_out,
            'width': bw,
            'height': bh
        })
        print_log(f"Optimized Background {os.path.basename(orig_path)}: {orig_size/1024:.1f} KB -> {bsize/1024:.1f} KB ({bw}x{bh})")

with open(os.path.join(assets_dir, 'log_data.json'), 'w') as f:
    json.dump(log_data, f, indent=2)

print_log("\nImage processing pipeline complete!")
