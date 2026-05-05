const mongoose = require('mongoose');

const contentSchema = new mongoose.Schema({
    page: { type: String, required: true }, // e.g., 'home', 'about', 'service-seo'
    key: { type: String, required: true },  // e.g., 'hero-title', 'footer-about'
    value: { type: String, required: true } // The actual content (HTML, text, or URL)
});

// Compound index to ensure uniqueness per page and key
contentSchema.index({ page: 1, key: 1 }, { unique: true });

module.exports = mongoose.model('Content', contentSchema);
