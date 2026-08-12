import os

public_dir = r'd:\creashiiftads\public'

mappings = {
    'service-seo': 'services/seo-services-kerala',
    'service-ads': 'services/google-ads-management',
    'service-social': 'services/social-media-marketing',
    'service-web': 'services/web-development-company',
    'service-design': 'services/graphic-design-branding',
    'service-video': 'services/video-production-services'
}

files_to_update = [
    'service-seo.html', 'service-ads.html', 'service-social.html', 'service-web.html', 'service-design.html', 'service-video.html',
    r'services\seo-services-kerala.html', r'services\google-ads-management.html', r'services\social-media-marketing.html',
    r'services\web-development-company.html', r'services\graphic-design-branding.html', r'services\video-production-services.html'
]

for rel_path in files_to_update:
    full_path = os.path.join(public_dir, rel_path)
    if os.path.exists(full_path):
        with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        updated = content
        for old_slug, new_slug in mappings.items():
            old_url = f'https://creashift.com/{old_slug}'
            new_url = f'https://creashift.com/{new_slug}'
            updated = updated.replace(old_url, new_url)

        if updated != content:
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(updated)
            print(f'Updated canonical & schema links in {rel_path}')
        else:
            print(f'No changes needed for {rel_path}')
