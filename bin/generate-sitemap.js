const fs = require('fs');
const path = require('path');
const mongoose = require('mongoose');
const dotenv = require('dotenv');

// Load environment variables
dotenv.config();

const PUBLIC_DIR = path.join(__dirname, '..', 'public');
const SITEMAP_PATH = path.join(PUBLIC_DIR, 'sitemap.xml');
const BASE_URL = 'https://creashift.com';

async function generateSitemapXml() {
  const files = fs.readdirSync(PUBLIC_DIR).filter(file => file.endsWith('.html'));
  
  // Exclude vault.html and blog-post.html (since articles are dynamically served under /blog/:slug)
  const excludedFiles = ['vault.html', 'blog-post.html'];
  const activeFiles = files.filter(f => !excludedFiles.includes(f));

  let xml = '<?xml version="1.0" encoding="UTF-8"?>\n';
  xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n';

  // 1. Static Pages
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

  // 2. Dynamic Article Slug Pages
  try {
    // Import Article Model
    const Article = require('../models/Article');
    const articles = await Article.find({}, 'slug updatedAt').sort({ createdAt: -1 });
    
    articles.forEach(article => {
      if (article.slug) {
        const lastmod = (article.updatedAt || new Date()).toISOString().split('T')[0];
        xml += '  <url>\n';
        xml += `    <loc>${BASE_URL}/blog/${article.slug}</loc>\n`;
        xml += `    <lastmod>${lastmod}</lastmod>\n`;
        xml += `    <changefreq>weekly</changefreq>\n`;
        xml += `    <priority>0.7</priority>\n`;
        xml += '  </url>\n';
      }
    });
  } catch (err) {
    console.error('Error fetching articles for sitemap:', err);
  }

  xml += '</urlset>\n';
  return xml;
}

// Standalone execution
if (require.main === module) {
  (async () => {
    try {
      if (mongoose.connection.readyState === 0) {
        await mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/creashift');
      }
      const xmlContent = await generateSitemapXml();
      fs.writeFileSync(SITEMAP_PATH, xmlContent, 'utf8');
      console.log(`Successfully generated dynamic sitemap at: ${SITEMAP_PATH}`);
      await mongoose.disconnect();
    } catch (error) {
      console.error('Error generating sitemap standalone:', error);
      process.exit(1);
    }
  })();
}

module.exports = { generateSitemapXml };
