import json, os

assets_dir = r'd:\creashiiftads\public\assets'
log_file = os.path.join(assets_dir, 'log_data.json')

if os.path.exists(log_file):
    with open(log_file) as f:
        data = json.load(f)

    total_orig = 0
    total_new = 0

    print("| Image Asset | Original Size | Optimized Size | Reduction | Width x Height |")
    print("| :--- | :---: | :---: | :---: | :---: |")

    for item in data:
        orig_kb = item['original_size'] / 1024
        new_kb = item['new_size'] / 1024
        total_orig += item['original_size']
        total_new += item['new_size']
        red_pct = ((orig_kb - new_kb) / orig_kb) * 100 if orig_kb > 0 else 0
        name = item['name']
        dim = f"{item['width']}x{item['height']}"
        print(f"| {name} | {orig_kb:.1f} KB | {new_kb:.1f} KB | **-{red_pct:.1f}%** | {dim} |")

    tot_orig_mb = total_orig / (1024 * 1024)
    tot_new_mb = total_new / (1024 * 1024)
    tot_red_pct = ((total_orig - total_new) / total_orig) * 100
    saved_mb = tot_orig_mb - tot_new_mb

    print(f"\nTOTAL ORIGINAL WEIGHT: {tot_orig_mb:.2f} MB")
    print(f"TOTAL OPTIMIZED WEIGHT: {tot_new_mb:.2f} MB")
    print(f"TOTAL PAYLOAD SAVED: {saved_mb:.2f} MB ({tot_red_pct:.1f}% Total Reduction)")
