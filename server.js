const express = require('express');
const mongoose = require('mongoose');
const session = require('express-session');
const passport = require('passport');
const GoogleStrategy = require('passport-google-oauth20').Strategy;
const path = require('path');
const dotenv = require('dotenv');
const cors = require('cors');
const nodemailer = require('nodemailer');
const Razorpay = require('razorpay');
const multer = require('multer');
const crypto = require('crypto');
const { v4: uuidv4 } = require('uuid');
const fs = require('fs');

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

// Ensure private_uploads directory exists
const privateUploadsDir = path.join(__dirname, 'private_uploads');
if (!fs.existsSync(privateUploadsDir)) {
    fs.mkdirSync(privateUploadsDir, { recursive: true });
}

// Razorpay Config
const razorpay = new Razorpay({
    key_id: process.env.RAZORPAY_KEY_ID || 'dummy_key_id',
    key_secret: process.env.RAZORPAY_KEY_SECRET || 'dummy_key_secret'
});

// Multer Config for secure file uploads
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, path.join(__dirname, 'private_uploads'));
    },
    filename: (req, file, cb) => {
        const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
        cb(null, uniqueSuffix + '-' + file.originalname);
    }
});
const upload = multer({ storage });

// Nodemailer Transporter
const transporter = nodemailer.createTransport({
    service: 'gmail',
    auth: {
        user: process.env.GMAIL_USER,
        pass: process.env.GMAIL_PASS // Google App Password
    }
});

// Connect to MongoDB
const connectDB = require('./db');
connectDB();

// Models
const Content = require('./models/Content');
const User = require('./models/User');
const Product = require('./models/Product');
const Order = require('./models/Order');

// Passport Config
passport.use(new GoogleStrategy({
    clientID: process.env.GOOGLE_CLIENT_ID || 'your_google_client_id',
    clientSecret: process.env.GOOGLE_CLIENT_SECRET || 'your_google_client_secret',
    callbackURL: process.env.GOOGLE_CALLBACK_URL || "http://localhost:3000/auth/google/callback",
    proxy: true
}, async (accessToken, refreshToken, profile, done) => {
    try {
        const email = profile.emails[0].value;
        const allowedAdmins = (process.env.ADMIN_EMAILS || "").split(',').map(e => e.trim().toLowerCase());
        
        // If the email is not in the allowed list, reject login
        if (!allowedAdmins.includes(email.toLowerCase())) {
            console.log(`Unauthorized login attempt from: ${email}`);
            return done(null, false, { message: 'Unauthorized email' });
        }

        let user = await User.findOne({ googleId: profile.id });
        if (!user) {
            user = await User.create({
                googleId: profile.id,
                displayName: profile.displayName,
                email: email
            });
        }
        return done(null, user);
    } catch (err) {
        return done(err, null);
    }
}));

passport.serializeUser((user, done) => done(null, user.id));
passport.deserializeUser(async (id, done) => {
    try {
        const user = await User.findById(id);
        done(null, user);
    } catch (err) {
        done(err, null);
    }
});

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(session({
    secret: process.env.SESSION_SECRET || 'secret_key',
    resave: false,
    saveUninitialized: false
}));
app.use(passport.initialize());
app.use(passport.session());

// Set View Engine
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Dynamic Sitemap Route
app.get('/sitemap.xml', (req, res) => {
    try {
        const { generateSitemapXml } = require('./bin/generate-sitemap');
        const xml = generateSitemapXml();
        res.header('Content-Type', 'application/xml');
        res.send(xml);
    } catch (err) {
        console.error('Error serving dynamic sitemap:', err);
        res.status(500).send('Error generating sitemap');
    }
});

// Static Files
app.use(express.static(path.join(__dirname, 'public'), { extensions: ['html'] }));

// Auth Routes
app.get('/auth/google', passport.authenticate('google', { scope: ['profile', 'email'] }));

app.get('/auth/google/callback', 
    passport.authenticate('google', { failureRedirect: '/login?error=unauthorized' }),
    (req, res) => res.redirect('/admin')
);

app.get('/logout', (req, res) => {
    req.logout((err) => {
        if (err) return next(err);
        res.redirect('/');
    });
});

// Auth Middleware
const isAdmin = (req, res, next) => {
    if (req.isAuthenticated()) return next();
    res.redirect('/login');
};

// Admin Routes
app.get('/login', (req, res) => {
    const error = req.query.error === 'unauthorized' ? 'Access Denied: Your email is not authorized.' : null;
    res.render('admin/login', { error });
});

app.get('/admin', isAdmin, async (req, res) => {
    const contents = await Content.find();
    res.render('admin/dashboard', { user: req.user, contents });
});

// API Routes for Content
app.get('/api/content/:page', async (req, res) => {
    try {
        const contents = await Content.find({ page: req.params.page });
        const contentMap = {};
        contents.forEach(item => {
            contentMap[item.key] = item.value;
        });
        res.json(contentMap);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

app.post('/api/content', isAdmin, async (req, res) => {
    const { page, key, value } = req.body;
    try {
        await Content.findOneAndUpdate(
            { page, key },
            { value },
            { upsert: true, new: true }
        );
        res.json({ success: true });
    } catch (err) {
        res.status(500).json({ success: false, error: err.message });
    }
});

app.post('/api/contact', async (req, res) => {
    const { name, email, phone, message } = req.body;

    const mailOptions = {
        from: process.env.GMAIL_USER,
        to: process.env.GMAIL_USER, // Send to yourself
        replyTo: email,
        subject: `New Lead: ${name}`,
        text: `Name: ${name}\nEmail: ${email}\nPhone: ${phone}\nMessage: ${message}`,
        html: `
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
                <h2 style="color: #333; text-align: center;">New Lead from Creashift</h2>
                <hr>
                <p><strong>Name:</strong> ${name}</p>
                <p><strong>Email:</strong> ${email}</p>
                <p><strong>Phone:</strong> ${phone}</p>
                <p style="margin-top: 20px;"><strong>Message:</strong></p>
                <div style="background: #f9f9f9; padding: 15px; border-radius: 5px;">
                    ${message}
                </div>
            </div>
        `
    };

    try {
        await transporter.sendMail(mailOptions);
        res.json({ success: true, message: 'Message sent successfully!' });
    } catch (error) {
        console.error('Error sending email:', error);
        res.status(500).json({ success: false, message: 'Failed to send message.' });
    }
});

// --- Vault Marketplace Routes ---

// Get active products
app.get('/api/vault/products', async (req, res) => {
    try {
        const products = await Product.find({ active: true }).select('-fileUrl');
        res.json(products);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// Create Razorpay Order
app.post('/api/payment/create', async (req, res) => {
    const { productId, customerEmail } = req.body;
    try {
        const product = await Product.findById(productId);
        if (!product) return res.status(404).json({ error: 'Product not found' });

        const options = {
            amount: product.price * 100, // amount in smallest currency unit (paise)
            currency: "INR",
            receipt: "order_rcptid_" + Date.now()
        };

        const order = await razorpay.orders.create(options);

        // Save pending order to DB
        await Order.create({
            customerEmail,
            productId,
            razorpayOrderId: order.id
        });

        res.json({
            orderId: order.id,
            amount: options.amount,
            currency: options.currency,
            key: process.env.RAZORPAY_KEY_ID || 'dummy_key_id'
        });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// Verify Payment and Generate Download Token
app.post('/api/payment/verify', async (req, res) => {
    const { razorpay_order_id, razorpay_payment_id, razorpay_signature } = req.body;
    try {
        const hmac = crypto.createHmac('sha256', process.env.RAZORPAY_KEY_SECRET || 'dummy_key_secret');
        hmac.update(razorpay_order_id + "|" + razorpay_payment_id);
        const generated_signature = hmac.digest('hex');

        if (generated_signature === razorpay_signature) {
            const downloadToken = uuidv4();
            
            await Order.findOneAndUpdate(
                { razorpayOrderId: razorpay_order_id },
                { 
                    status: 'completed',
                    razorpayPaymentId: razorpay_payment_id,
                    downloadToken: downloadToken
                }
            );

            res.json({ success: true, downloadToken });
        } else {
            res.status(400).json({ success: false, error: 'Invalid signature' });
        }
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// Secure Download Route
app.get('/api/download/:token', async (req, res) => {
    try {
        const order = await Order.findOne({ downloadToken: req.params.token }).populate('productId');
        if (!order || order.status !== 'completed') {
            return res.status(403).send('Invalid or expired download link.');
        }

        const filePath = path.join(__dirname, 'private_uploads', order.productId.fileUrl);
        if (!fs.existsSync(filePath)) {
            return res.status(404).send('File not found on server.');
        }

        res.download(filePath);
    } catch (err) {
        res.status(500).send('Server Error');
    }
});

// --- Vault Admin Routes ---

// Upload a new product
app.post('/api/admin/products', isAdmin, upload.single('productFile'), async (req, res) => {
    try {
        const { title, description, category, price, coverImage } = req.body;
        const fileUrl = req.file ? req.file.filename : '';

        if (!fileUrl) return res.status(400).json({ error: 'File upload is required.' });

        await Product.create({
            title,
            description,
            category,
            price: Number(price),
            fileUrl,
            coverImage
        });

        res.json({ success: true });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// List all products for admin
app.get('/api/admin/products', isAdmin, async (req, res) => {
    try {
        const products = await Product.find();
        res.json(products);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// Delete a product
app.delete('/api/admin/products/:id', isAdmin, async (req, res) => {
    try {
        const product = await Product.findById(req.params.id);
        if (product && product.fileUrl) {
            const filePath = path.join(__dirname, 'private_uploads', product.fileUrl);
            if (fs.existsSync(filePath)) {
                fs.unlinkSync(filePath);
            }
        }
        await Product.findByIdAndDelete(req.params.id);
        res.json({ success: true });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// Serve HTML files as dynamic pages (optional, or just serve them static)
// For now, we serve them as static, and they fetch content via API.

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT} [${process.env.NODE_ENV || 'development'}]`);
});
