const express = require('express');
const mongoose = require('mongoose');
const session = require('express-session');
const passport = require('passport');
const GoogleStrategy = require('passport-google-oauth20').Strategy;
const path = require('path');
const dotenv = require('dotenv');
const cors = require('cors');
const nodemailer = require('nodemailer');

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

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

// Passport Config
passport.use(new GoogleStrategy({
    clientID: process.env.GOOGLE_CLIENT_ID || 'your_google_client_id',
    clientSecret: process.env.GOOGLE_CLIENT_SECRET || 'your_google_client_secret',
    callbackURL: "https://creashift.com/auth/google/callback",
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

// Serve HTML files as dynamic pages (optional, or just serve them static)
// For now, we serve them as static, and they fetch content via API.

app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
