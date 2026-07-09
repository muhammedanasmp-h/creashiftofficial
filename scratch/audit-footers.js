const fs = require('fs');
const path = require('path');

const PUBLIC_DIR = path.join(__dirname, '..', 'public');
const files = fs.readdirSync(PUBLIC_DIR).filter(file => file.endsWith('.html'));

files.forEach(filename => {
  const filePath = path.join(PUBLIC_DIR, filename);
  const content = fs.readFileSync(filePath, 'utf8');

  const footerCount = (content.match(/<footer\b/gi) || []).length;
  if (footerCount > 1) {
    console.log(`⚠️ ${filename} has ${footerCount} footer tags!`);
  } else {
    console.log(`✅ ${filename} has ${footerCount} footer tag.`);
  }
});
