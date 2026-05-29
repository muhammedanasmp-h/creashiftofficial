const mongoose = require('mongoose');

const productSchema = new mongoose.Schema({
    title: { type: String, required: true },
    description: { type: String, required: true },
    category: { type: String, required: true },
    price: { type: Number, required: true }, // Price in smallest currency unit (e.g. paise for INR) or normal, depends on Razorpay setup. Let's assume standard float/int and convert later. Let's say price in INR.
    fileUrl: { type: String, required: true }, // Path in private_uploads
    coverImage: { type: String, required: true }, // Path in public/assets or base64 or URL
    active: { type: Boolean, default: true },
    createdAt: { type: Date, default: Date.now }
});

module.exports = mongoose.model('Product', productSchema);
