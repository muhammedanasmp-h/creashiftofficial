const fs = require('fs');
const path = require('path');
const publicDir = 'd:\\creashiiftads\\public';
const files = [
  'service-seo.html', 'service-ads.html', 'service-social.html', 'service-web.html', 'service-design.html', 'service-video.html',
  'services/seo-services-kerala.html', 'services/google-ads-management.html', 'services/social-media-marketing.html',
  'services/web-development-company.html', 'services/graphic-design-branding.html', 'services/video-production-services.html'
];
files.forEach(f => {
  const p = path.join(publicDir, f);
  if (fs.existsSync(p)) {
    const c = fs.readFileSync(p, 'utf8');
    const canonMatch = c.match(/<link\s+rel=["']canonical["']\s+href=["']([^"']+)["']/i);
    const ogMatch = c.match(/<meta\s+property=["']og:url["']\s+content=["']([^"']+)["']/i);
    console.log(f + ' => canonical: ' + (canonMatch ? canonMatch[1] : 'NONE') + ' | og:url: ' + (ogMatch ? ogMatch[1] : 'NONE'));
  }
});
