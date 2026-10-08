const fs = require('fs');
const path = require('path');

const DEFAULT_CONTACTS = {
    'contact-whatsapp': '+91 80861 80780',
    'contact-primary-phone': '+91 80861 80780',
    'contact-footer-phone-1': '+91 62828 52686',
    'contact-footer-phone-2': '+91 90742 99942',
    'contact-email': 'sales@creashift.in'
};

const cleanDigits = (val) => {
    return (val || '').replace(/\D/g, '');
};

const cleanTel = (val) => {
    const raw = (val || '').trim();
    const hasPlus = raw.startsWith('+');
    const digits = raw.replace(/\D/g, '');
    return hasPlus ? `+${digits}` : `+${digits}`;
};

// Retrieve contact numbers from DB, falling back to defaults
async function getContactNumbers(ContentModel) {
    const result = { ...DEFAULT_CONTACTS };
    try {
        if (ContentModel) {
            const records = await ContentModel.find({
                page: { $in: ['contact', 'contact-numbers'] }
            });
            records.forEach(doc => {
                if (doc.key && result.hasOwnProperty(doc.key)) {
                    result[doc.key] = doc.value;
                }
            });
        }
    } catch (err) {
        console.error('Error fetching contact numbers from DB:', err.message);
    }
    return result;
}

// Recursively get all HTML files in a directory
function getHtmlFiles(dir, fileList = []) {
    if (!fs.existsSync(dir)) return fileList;
    const files = fs.readdirSync(dir);
    for (const file of files) {
        const filePath = path.join(dir, file);
        const stat = fs.statSync(filePath);
        if (stat.isDirectory()) {
            if (file !== 'node_modules' && file !== '.git') {
                getHtmlFiles(filePath, fileList);
            }
        } else if (file.endsWith('.html')) {
            fileList.push(filePath);
        }
    }
    return fileList;
}

// Sync contact numbers across all static HTML files
function syncContactsToHtmlFiles(contacts) {
    const active = { ...DEFAULT_CONTACTS, ...contacts };
    const waDigits = cleanDigits(active['contact-whatsapp']) || '918086180780';
    const waUrl = `https://wa.me/${waDigits}`;
    const primaryPhone = active['contact-primary-phone'] || '+91 80861 80780';
    const primaryTel = `tel:${cleanTel(primaryPhone)}`;
    const footerPhone1 = active['contact-footer-phone-1'] || '+91 62828 52686';
    const footerTel1 = `tel:${cleanTel(footerPhone1)}`;
    const footerPhone2 = active['contact-footer-phone-2'] || '+91 90742 99942';
    const footerTel2 = `tel:${cleanTel(footerPhone2)}`;
    const email = active['contact-email'] || 'sales@creashift.in';
    const mailto = `mailto:${email}`;

    const publicDir = path.join(__dirname, '..', 'public');
    const htmlFiles = getHtmlFiles(publicDir);

    let updatedCount = 0;

    for (const file of htmlFiles) {
        try {
            let content = fs.readFileSync(file, 'utf8');
            let modified = false;

            // 1. WhatsApp Links (wa.me/...)
            const waRegex = /href=["']https:\/\/wa\.me\/\d+["']/g;
            if (waRegex.test(content)) {
                content = content.replace(waRegex, `href="${waUrl}"`);
                modified = true;
            }

            // 2. Footer Phone 1: update tel link and displayed text
            // Match any tel: link with digits around 62828 or previously tagged data-contact="footer-phone-1"
            const taggedPhone1 = /(<a\s+[^>]*data-contact=["']footer-phone-1["'][^>]*href=["'])tel:[^"']+([^>]*>)([^<]*)(<\/a>)/gi;
            if (taggedPhone1.test(content)) {
                content = content.replace(taggedPhone1, `$1${footerTel1}$2${footerPhone1}$4`);
                modified = true;
            }

            // Also match untagged footer phone 1 patterns
            const untaggedPhone1 = /<a\s+href=["']tel:\+?91\s*62828\s*52686["']([^>]*)>([^<]*)<\/a>/gi;
            if (untaggedPhone1.test(content)) {
                content = content.replace(untaggedPhone1, `<a href="${footerTel1}" data-contact="footer-phone-1"$1>${footerPhone1}</a>`);
                modified = true;
            }

            // 3. Footer Phone 2: update tel link and displayed text
            const taggedPhone2 = /(<a\s+[^>]*data-contact=["']footer-phone-2["'][^>]*href=["'])tel:[^"']+([^>]*>)([^<]*)(<\/a>)/gi;
            if (taggedPhone2.test(content)) {
                content = content.replace(taggedPhone2, `$1${footerTel2}$2${footerPhone2}$4`);
                modified = true;
            }

            const untaggedPhone2 = /<a\s+href=["']tel:\+?91\s*90742\s*99942["']([^>]*)>([^<]*)<\/a>/gi;
            if (untaggedPhone2.test(content)) {
                content = content.replace(untaggedPhone2, `<a href="${footerTel2}" data-contact="footer-phone-2"$1>${footerPhone2}</a>`);
                modified = true;
            }

            // 4. Primary Contact Call link (contact.html)
            const taggedPrimary = /(<a\s+[^>]*data-contact=["']primary-phone["'][^>]*href=["'])tel:[^"']+([^>]*>)/gi;
            if (taggedPrimary.test(content)) {
                content = content.replace(taggedPrimary, `$1${primaryTel}$2`);
                modified = true;
            }

            const untaggedPrimary = /(<a\s+(?![^>]*data-contact=["']primary-phone["'])[^>]*href=["'])tel:\+?91\s*80861\s*80780(["'][^>]*>)/gi;
            if (untaggedPrimary.test(content)) {
                content = content.replace(untaggedPrimary, `$1${primaryTel}" data-contact="primary-phone$2`);
                modified = true;
            }

            // Clean up any duplicate data-contact attributes if present
            if (content.includes('data-contact="primary-phone" data-contact="primary-phone"')) {
                content = content.replace(/data-contact=["']primary-phone["']\s+data-contact=["']primary-phone["']/g, 'data-contact="primary-phone"');
                modified = true;
            }

            // 5. Email link
            const taggedEmail = /(<a\s+[^>]*data-contact=["']email["'][^>]*href=["'])mailto:[^"']+([^>]*>)([^<]*)(<\/a>)/gi;
            if (taggedEmail.test(content)) {
                content = content.replace(taggedEmail, `$1${mailto}$2${email}$4`);
                modified = true;
            }

            const untaggedEmail = /<a\s+href=["']mailto:sales@creashift\.in["']([^>]*)>([^<]*)<\/a>/gi;
            if (untaggedEmail.test(content)) {
                content = content.replace(untaggedEmail, `<a href="${mailto}" data-contact="email"$1>${email}</a>`);
                modified = true;
            }

            // 6. JSON-LD schema telephone fields
            const schemaPhone = /"telephone":\s*"[^"]*"/g;
            if (schemaPhone.test(content)) {
                content = content.replace(schemaPhone, `"telephone": "${footerPhone1}"`);
                modified = true;
            }

            // 7. Tag WhatsApp float and links with data-contact="whatsapp" if not already tagged
            const untaggedWa = /(<a\s+[^>]*href=["']https:\/\/wa\.me\/[^"']+["'])(?![^>]*data-contact)([^>]*>)/gi;
            if (untaggedWa.test(content)) {
                content = content.replace(untaggedWa, `$1 data-contact="whatsapp"$2`);
                modified = true;
            }

            // 8. Ensure contact-sync.js script tag is included before </body>
            if (!content.includes('contact-sync.js')) {
                if (content.includes('</body>')) {
                    content = content.replace('</body>', '    <script src="/assets/js/contact-sync.js" defer></script>\n</body>');
                    modified = true;
                }
            }

            if (modified) {
                fs.writeFileSync(file, content, 'utf8');
                updatedCount++;
            }
        } catch (err) {
            console.error(`Error syncing contact numbers in ${file}:`, err.message);
        }
    }
    return { updatedCount, totalFiles: htmlFiles.length };
}

// Save contact numbers to DB and sync to HTML files
async function saveContactNumbers(ContentModel, updates) {
    const keys = Object.keys(DEFAULT_CONTACTS);
    const saved = {};

    for (const key of keys) {
        if (updates.hasOwnProperty(key) && updates[key] !== undefined && updates[key] !== null) {
            const val = String(updates[key]).trim();
            saved[key] = val;
            if (ContentModel) {
                await ContentModel.findOneAndUpdate(
                    { page: 'contact', key },
                    { page: 'contact', key, value: val },
                    { upsert: true, new: true }
                );
                await ContentModel.findOneAndUpdate(
                    { page: 'contact-numbers', key },
                    { page: 'contact-numbers', key, value: val },
                    { upsert: true, new: true }
                );
            }
        }
    }

    // Now sync to HTML files with complete merged state
    const current = await getContactNumbers(ContentModel);
    const syncResult = syncContactsToHtmlFiles(current);

    return {
        success: true,
        data: current,
        sync: syncResult
    };
}

module.exports = {
    DEFAULT_CONTACTS,
    cleanDigits,
    cleanTel,
    getContactNumbers,
    syncContactsToHtmlFiles,
    saveContactNumbers
};
