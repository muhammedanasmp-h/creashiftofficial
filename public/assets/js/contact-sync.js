/**
 * CREASHIFT - Dynamic Contact Numbers Client Sync
 * Automatically ensures all contact numbers, WhatsApp links, and footers
 * stay updated across all pages in real-time.
 */
(function () {
    const STORAGE_KEY = 'creashift_contacts_v1';

    function cleanDigits(val) {
        return (val || '').replace(/\D/g, '');
    }

    function cleanTel(val) {
        const raw = (val || '').trim();
        const hasPlus = raw.startsWith('+');
        const digits = raw.replace(/\D/g, '');
        return hasPlus ? `+${digits}` : `+${digits}`;
    }

    function applyContacts(data) {
        if (!data || typeof data !== 'object') return;

        const waRaw = data['contact-whatsapp'] || '+91 80861 80780';
        const waDigits = cleanDigits(waRaw) || '918086180780';
        const waUrl = `https://wa.me/${waDigits}`;

        const primaryPhone = data['contact-primary-phone'] || '+91 80861 80780';
        const primaryTel = `tel:${cleanTel(primaryPhone)}`;

        const footerPhone1 = data['contact-footer-phone-1'] || '+91 62828 52686';
        const footerTel1 = `tel:${cleanTel(footerPhone1)}`;

        const footerPhone2 = data['contact-footer-phone-2'] || '+91 90742 99942';
        const footerTel2 = `tel:${cleanTel(footerPhone2)}`;

        const email = data['contact-email'] || 'sales@creashift.in';
        const mailto = `mailto:${email}`;

        // 1. WhatsApp Links (Float button, drawer, CTAs, footer)
        document.querySelectorAll('a[href*="wa.me"], a[data-contact="whatsapp"], #whatsappFloat').forEach(el => {
            el.href = waUrl;
        });

        // 2. Footer Phone 1
        document.querySelectorAll('a[data-contact="footer-phone-1"]').forEach(el => {
            el.href = footerTel1;
            el.textContent = footerPhone1;
        });

        // 3. Footer Phone 2
        document.querySelectorAll('a[data-contact="footer-phone-2"]').forEach(el => {
            el.href = footerTel2;
            el.textContent = footerPhone2;
        });

        // 4. Primary Contact Phone (Contact Page Call Card)
        document.querySelectorAll('a[data-contact="primary-phone"], a[href^="tel:+918086180780"]').forEach(el => {
            el.href = primaryTel;
            if (el.hasAttribute('data-show-phone-text')) {
                el.textContent = primaryPhone;
            }
        });

        // 5. Email Links
        document.querySelectorAll('a[data-contact="email"], a[href^="mailto:sales@creashift.in"]').forEach(el => {
            el.href = mailto;
            if (el.textContent.includes('@')) {
                el.textContent = email;
            }
        });

        // Fire custom event
        try {
            window.dispatchEvent(new CustomEvent('creashift:contacts-updated', { detail: data }));
        } catch (e) {}
    }

    // Immediate cached run to prevent layout shift
    try {
        const cached = sessionStorage.getItem(STORAGE_KEY);
        if (cached) {
            applyContacts(JSON.parse(cached));
        }
    } catch (e) {}

    // Fetch fresh contacts from server
    function fetchAndApply() {
        fetch('/api/contact-numbers', { cache: 'no-store' })
            .then(res => {
                if (!res.ok) throw new Error('Network error');
                return res.json();
            })
            .then(data => {
                if (data && typeof data === 'object') {
                    try {
                        sessionStorage.setItem(STORAGE_KEY, JSON.stringify(data));
                    } catch (e) {}
                    applyContacts(data);
                }
            })
            .catch(() => {
                // Silently keep current DOM values if offline
            });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', fetchAndApply);
    } else {
        fetchAndApply();
    }
})();
