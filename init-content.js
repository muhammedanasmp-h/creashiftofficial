require('dotenv').config();
const mongoose = require('mongoose');
const Content = require('./models/Content');

const MONGODB_URI = process.env.MONGODB_URI;

const initialContent = [
    // Services Page
    { page: 'services', key: 'services-headline', value: 'PRECISION STRATEGY.' },
    { page: 'services', key: 'services-subtext', value: 'Our approach combines architectural rigor with fluid digital execution. We specialize in high-stakes branding and high-performance technology.' },
    { page: 'services', key: 'services-card-seo-title', value: 'SEO & Search Architecture' },
    { page: 'services', key: 'services-card-seo-desc', value: "Architecting digital visibility through technical precision and algorithmic intelligence. We don't just chase rankings; we dominate search landscapes." },
    { page: 'services', key: 'services-card-social-title', value: 'Social Ecosystems' },
    { page: 'services', key: 'services-card-social-desc', value: 'Building communities that advocate for your brand through cultural resonance.' },
    { page: 'services', key: 'services-card-web-title', value: 'Web Engineering' },
    { page: 'services', key: 'services-card-web-desc', value: 'Architectural digital platforms built for performance and luxury conversion.' },
    { page: 'services', key: 'services-card-ads-title', value: 'Paid Ads & Growth' },
    { page: 'services', key: 'services-card-ads-desc', value: 'Scaling brands through data-driven aggressive targeting and high-conversion assets.' },
    { page: 'services', key: 'services-card-design-title', value: 'Design & Identity' },
    { page: 'services', key: 'services-card-video-title', value: 'Video Production' },

    // SEO Detail Page
    { page: 'service-seo', key: 'seo-headline', value: 'Search Engine Optimization' },
    { page: 'service-seo', key: 'seo-intro', value: 'Architecting digital authority through technical precision and algorithmic intelligence to ensure your brand dominates search landscapes.' },
    { page: 'service-seo', key: 'seo-sub-headline', value: 'Precision Visibility' },
    { page: 'service-seo', key: 'seo-sub-intro', value: "We don't just chase rankings; we architect digital dominance. Our SEO strategy is built on the intersection of technical precision and competitive intelligence." },
    { page: 'service-seo', key: 'seo-card-1-title', value: 'Technical Architecture' },
    { page: 'service-seo', key: 'seo-card-1-desc', value: "Deep-level audits ensuring your site's foundation is perfectly indexed and performance-optimized." },
    { page: 'service-seo', key: 'seo-card-2-title', value: 'Keyword Intelligence' },
    { page: 'service-seo', key: 'seo-card-2-desc', value: 'Targeting high-intent clusters that drive actual business conversion and sustainable growth.' },

    // Social Detail Page
    { page: 'service-social', key: 'social-headline', value: 'Social Media Marketing' },
    { page: 'service-social', key: 'social-intro', value: 'Bridging the gap between brand identity and cultural relevance through high-impact storytelling and community engineering.' },
    { page: 'service-social', key: 'social-sub-headline', value: 'Cultural Relevance' },
    { page: 'service-social', key: 'social-sub-intro', value: 'Engagement is the new currency. We build communities, not just follower counts. Our social strategy creates content that is meant to be shared, discussed, and remembered.' },
    { page: 'service-social', key: 'social-card-1-title', value: 'Persona Mapping' },
    { page: 'service-social', key: 'social-card-1-desc', value: 'Defining exactly who your audience is and what triggers their engagement.' },
    { page: 'service-social', key: 'social-card-2-title', value: 'Viral Analytics' },
    { page: 'service-social', key: 'social-card-2-desc', value: 'Monitoring trends in real-time to capitalize on moments that matter.' },

    // Web Detail Page
    { page: 'service-web', key: 'web-headline', value: 'Web Design & Development' },
    { page: 'service-web', key: 'web-intro', value: 'Building architectural digital masterpieces that convert visitors into lifelong advocates through structural precision.' },
    { page: 'service-web', key: 'web-sub-headline', value: 'Digital Masterpieces' },
    { page: 'service-web', key: 'web-sub-intro', value: 'Our websites are built to be high-performance conversion machines that feel like luxury experiences. Every pixel is intentional.' },
    { page: 'service-web', key: 'web-card-1-title', value: 'UX Blueprint' },
    { page: 'service-web', key: 'web-card-1-desc', value: 'Rigorous wireframing to ensure the user journey is frictionless and intuitive. We map every touchpoint.' },
    { page: 'service-web', key: 'web-card-2-title', value: 'UI Craft' },
    { page: 'service-web', key: 'web-card-2-desc', value: "Boutique visual design that reflects your brand's unique identity and authority. Premium aesthetics." },
    { page: 'service-web', key: 'web-card-3-title', value: 'Performance' },
    { page: 'service-web', key: 'web-card-3-desc', value: 'Clean, scalable code optimized for speed, security, and future growth. Built for the modern web.' },

    // Ads Detail Page
    { page: 'service-ads', key: 'ads-headline', value: 'Paid Ads (Meta & Google)' },
    { page: 'service-ads', key: 'ads-intro', value: 'Scaling brands through data-driven aggressive targeting and high-conversion assets. We turn ad spend into measurable revenue.' },
    { page: 'service-ads', key: 'ads-sub-headline', value: 'Aggressive Growth' },
    { page: 'service-ads', key: 'ads-sub-intro', value: 'Growth is a science. We use aggressive targeting and high-converting visual assets to ensure your ad spend delivers maximum ROI.' },
    { page: 'service-ads', key: 'ads-metric-1-value', value: '350%+' },
    { page: 'service-ads', key: 'ads-metric-1-label', value: 'Average ROI Increase' },
    { page: 'service-ads', key: 'ads-metric-2-value', value: '45%' },
    { page: 'service-ads', key: 'ads-metric-2-label', value: 'Reduction in CPA' },

    // Design Detail Page
    { page: 'service-design', key: 'design-headline', value: 'Brand Identity & Design' },
    { page: 'service-design', key: 'design-intro', value: 'Crafting visual legacies that resonate through minimalist luxury and structural precision. We build brands that command space.' },
    { page: 'service-design', key: 'design-sub-headline', value: 'Visual Dominance' },
    { page: 'service-design', key: 'design-sub-intro', value: 'Design is the final word. We create brand identities that are perceived as the authority they are.' },
    { page: 'service-design', key: 'design-card-1-title', value: 'Identity Systems' },
    { page: 'service-design', key: 'design-card-1-desc', value: 'Complete visual frameworks from logo suites to typography.' },
    { page: 'service-design', key: 'design-card-2-title', value: 'Design Language' },
    { page: 'service-design', key: 'design-card-2-desc', value: 'Curating visual motifs that evoke premium positioning.' },

    // Video Detail Page
    { page: 'service-video', key: 'video-headline', value: 'Video Production & Reels' },
    { page: 'service-video', key: 'video-intro', value: 'Capturing the essence of your brand through cinematic motion and high-conversion vertical storytelling.' },
    { page: 'service-video', key: 'video-sub-headline', value: 'Motion Heritage' },
    { page: 'service-video', key: 'video-sub-intro', value: 'Movement is the ultimate attention-grabber. We produce visual assets that build desire.' },
    { page: 'service-video', key: 'video-card-1-title', value: 'Cinematic Ads' },
    { page: 'service-video', key: 'video-card-1-desc', value: 'High-end production commercials that position you as a leader.' },
    { page: 'service-video', key: 'video-card-2-title', value: 'Viral Reels' },
    { page: 'service-video', key: 'video-card-2-desc', value: 'Engineered for engagement and brand recall.' }
];

async function init() {
    try {
        await mongoose.connect(MONGODB_URI);
        console.log('Connected to MongoDB');

        for (const item of initialContent) {
            await Content.findOneAndUpdate(
                { page: item.page, key: item.key },
                item,
                { upsert: true, new: true }
            );
            console.log(`Initialized: ${item.page} -> ${item.key}`);
        }

        console.log('Database initialization complete!');
        process.exit(0);
    } catch (err) {
        console.error('Error initializing database:', err);
        process.exit(1);
    }
}

init();
