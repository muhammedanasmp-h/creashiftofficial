const mongoose = require('mongoose');

const articleSchema = new mongoose.Schema({
    title: { type: String, required: true },
    summary: { type: String, required: true },
    description: { type: String, required: true },
    category: { type: String, required: true }, // e.g., 'strategy', 'design', 'technology', 'case-studies'
    imageUrl: { type: String, required: true },
    isFeatured: { type: Boolean, default: false },
    slug: { type: String, required: true, unique: true },
    metaTitle: { type: String },
    metaDescription: { type: String },
    focusKeyword: { type: String }
}, { timestamps: true });

module.exports = mongoose.model('Article', articleSchema);
