const mongoose = require('mongoose');

const articleSchema = new mongoose.Schema({
    title: { type: String, required: true },
    summary: { type: String, required: true },
    category: { type: String, required: true }, // e.g., 'strategy', 'design', 'technology', 'case-studies'
    imageUrl: { type: String, required: true }
}, { timestamps: true });

module.exports = mongoose.model('Article', articleSchema);
