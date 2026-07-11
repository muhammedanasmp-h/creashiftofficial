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
            if (page === 'blog-premium') {
                fetchArticles();
            }
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

            // [NEW] Special handling for Categories to enable Filtering
            if (key.endsWith('-cat')) {
                const containerId = key.split('-cat')[0];
                const container = document.getElementById(containerId);
                if (container) {
                    container.setAttribute('data-category', value.toLowerCase());
                }
            }
        });

        // Initialize filters after content is applied
        initFilters();
    }

    function initFilters() {
        const filterBtns = document.querySelectorAll('.filter-btn');
        const items = document.querySelectorAll('.masonry-item');

        if (filterBtns.length === 0) return;

        filterBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const filter = btn.getAttribute('data-filter');
                
                // Update button UI
                filterBtns.forEach(b => {
                    b.classList.remove('bg-black', 'text-white');
                    b.classList.add('text-on-surface');
                });
                btn.classList.add('bg-black', 'text-white');
                btn.classList.remove('text-on-surface');

                // Filter items
                items.forEach(item => {
                    const cat = item.getAttribute('data-category');
                    if (filter === 'all' || cat === filter) {
                        item.style.display = 'block';
                        setTimeout(() => { item.style.opacity = '1'; item.style.transform = 'scale(1)'; }, 10);
                    } else {
                        item.style.opacity = '0';
                        item.style.transform = 'scale(0.95)';
                        setTimeout(() => { item.style.display = 'none'; }, 300);
                    }
                });
            });
        });
    }

    function fetchArticles() {
        fetch('/api/articles')
            .then(res => res.json())
            .then(articles => {
                const sidebarContainer = document.getElementById('dynamic-sidebar-container');
                const gridContainer = document.getElementById('dynamic-grid-container');
                if (!sidebarContainer || !gridContainer) return;

                if (articles.length > 0) {
                    const firstArticle = articles[0];
                    sidebarContainer.innerHTML = `
                        <article class="masonry-item group cursor-pointer" data-category="${firstArticle.category.toLowerCase()}">
                            <div class="mb-8 overflow-hidden aspect-square bg-gray-50">
                                <img alt="${firstArticle.title}" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700 ease-out" src="${firstArticle.imageUrl || 'https://via.placeholder.com/600'}"/>
                            </div>
                            <span class="font-label-sm text-[10px] text-gray-400 mb-4 block uppercase tracking-widest"><span>${firstArticle.category}</span></span>
                            <h3 class="text-2xl font-bold mb-4 leading-tight">${firstArticle.title}</h3>
                            <p class="text-gray-500 text-sm leading-relaxed line-clamp-2">${firstArticle.summary}</p>
                        </article>
                    `;
                }

                if (articles.length > 1) {
                    const restArticles = articles.slice(1);
                    gridContainer.innerHTML = restArticles.map(article => `
                        <article class="masonry-item group flex flex-col" data-category="${article.category.toLowerCase()}">
                            <div class="mb-8 overflow-hidden aspect-[1/1] bg-gray-50">
                                <img alt="${article.title}" class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700 ease-out" src="${article.imageUrl || 'https://via.placeholder.com/600'}"/>
                            </div>
                            <span class="font-label-sm text-[10px] text-black mb-4 uppercase"><span>${article.category}</span></span>
                            <h3 class="text-xl font-semibold mb-4 leading-snug">${article.title}</h3>
                            <p class="text-gray-500 text-sm line-clamp-3 mb-6">${article.summary}</p>
                        </article>
                    `).join('');
                }
                
                // Re-initialize filters for the dynamically added items
                initFilters();
            })
            .catch(err => console.error('Error fetching dynamic articles:', err));
    }
});
