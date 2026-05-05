/**
 * CREASHIFT Content Manager
 * Fetches dynamic content from the backend and applies it to the DOM.
 */

document.addEventListener('DOMContentLoaded', () => {
    // Identify the current page based on the filename or a data attribute
    const path = window.location.pathname;
    let page = 'home';
    
    if (path.includes('about')) page = 'about';
    else if (path.includes('services')) page = 'services';
    else if (path.includes('portfolio')) page = 'portfolio';
    else if (path.includes('contact')) page = 'contact';
    else if (path.includes('service-seo')) page = 'service-seo';
    else if (path.includes('service-social')) page = 'service-social';
    else if (path.includes('service-web')) page = 'service-web';
    else if (path.includes('service-ads')) page = 'service-ads';
    else if (path.includes('service-design')) page = 'service-design';
    else if (path.includes('service-video')) page = 'service-video';
    else if (path.includes('blog-premium')) page = 'blog-premium';
    else if (path === '/' || path.includes('index')) page = 'home';

    // Skip dynamic loading for Home and About as requested
    if (page === 'home' || page === 'about') {
        console.log('Static page detected, skipping dynamic content loading.');
        return;
    }

    // Fetch content from API
    fetch(`/api/content/${page}`)
        .then(response => response.json())
        .then(contentMap => {
            applyContent(contentMap);
        })
        .catch(err => console.error('Error fetching dynamic content:', err));

    function applyContent(contentMap) {
        Object.keys(contentMap).forEach(key => {
            const element = document.getElementById(key);
            if (!element) return;

            const value = contentMap[key];
            
            // Apply based on element type
            if (element.tagName === 'IMG') {
                element.src = value;
            } else if (element.tagName === 'A') {
                // If it's a link, we might want to change text or href. 
                // For now, let's assume innerHTML unless it's specifically a URL field
                if (key.endsWith('-url')) {
                    element.href = value;
                } else {
                    element.innerHTML = value;
                }
            } else if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
                element.value = value;
            } else {
                element.innerHTML = value;
            }
        });
    }
});
