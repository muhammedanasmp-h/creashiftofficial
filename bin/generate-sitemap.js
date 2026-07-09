const fs = require('fs');
const path = require('path');

const PUBLIC_DIR = path.join(__dirname, '..', 'public');
const SITEMAP_PATH = path.join(PUBLIC_DIR, 'sitemap.xml');
const BASE_URL = 'https://creashift.com';

function generateSitemapXml() {
  const files = fs.readdirSync(PUBLIC_DIR).filter(file => file.endsWith('.html'));
  
  // Exclude vault.html since it is noindex, nofollow
  const excludedFiles = ['vault.html'];
  const activeFiles = files.filter(f => !excludedFiles.includes(f));

  let xml = '<?xml version="1.0" encoding="UTF-8"?>\n';
  xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n';

  activeFiles.forEach(filename => {
    const filePath = path.join(PUBLIC_DIR, filename);
    const stats = fs.statSync(filePath);
    const lastmod = stats.mtime.toISOString().split('T')[0];

    // Build clean URL
    let cleanPath = '';
    if (filename !== 'index.html') {
      cleanPath = '/' + filename.replace('.html', '');
    }
    const loc = `${BASE_URL}${cleanPath}`;

    // Determine priority and changefreq based on page type
    let priority = '0.8';
    let changefreq = 'weekly';

    if (filename === 'index.html') {
      priority = '1.0';
      changefreq = 'daily';
    } else if (filename.startsWith('service-')) {
      priority = '0.9';
      changefreq = 'weekly';
    } else if (['terms.html', 'agreement.html', 'privacy.html'].includes(filename)) {
      priority = '0.3';
      changefreq = 'monthly';
    }

    xml += '  <url>\n';
    xml += `    <loc>${loc}</loc>\n`;
    xml += `    <lastmod>${lastmod}</lastmod>\n`;
    xml += `    <changefreq>${changefreq}</changefreq>\n`;
    xml += `    <priority>${priority}</priority>\n`;
    xml += '  </url>\n';
  });

  xml += '</urlset>\n';
  return xml;
}

// Generate and write sitemap
try {
  const xmlContent = generateSitemapXml();
  fs.writeFileSync(SITEMAP_PATH, xmlContent, 'utf8');
  console.log(`Successfully generated dynamic sitemap at: ${SITEMAP_PATH}`);
} catch (error) {
  console.error('Error generating sitemap:', error);
  process.exit(1);
}

module.exports = { generateSitemapXml };
