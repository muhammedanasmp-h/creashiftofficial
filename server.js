const express = require('express');
const mongoose = require('mongoose');
const session = require('express-session');
const passport = require('passport');
const GoogleStrategy = require('passport-google-oauth20').Strategy;
const path = require('path');
const dotenv = require('dotenv');
const cors = require('cors');

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

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
    callbackURL: "/auth/google/callback"
}, async (accessToken, refreshToken, profile, done) => {
    try {
        let user = await User.findOne({ googleId: profile.id });
        if (!user) {
            // In a real scenario, you might want to restrict this to specific emails
            user = await User.create({
                googleId: profile.id,
                displayName: profile.displayName,
                email: profile.emails[0].value
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
    passport.authenticate('google', { failureRedirect: '/login' }),
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
    res.render('admin/login');
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

// Serve HTML files as dynamic pages (optional, or just serve them static)
// For now, we serve them as static, and they fetch content via API.

app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
