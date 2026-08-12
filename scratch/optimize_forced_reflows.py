import os, re

index_path = r'd:\creashiiftads\public\index.html'
about_path = r'd:\creashiiftads\public\about.html'

# 1. Optimize index.html
with open(index_path, 'r', encoding='utf-8') as f:
    index_content = f.read()

# Replace reviews-container script block
reviews_pattern = re.compile(
    r'// Reviews Auto-slide with IntersectionObserver.*?(?=window\.addEventListener\(\'DOMContentLoaded\')',
    re.DOTALL
)

optimized_reviews_script = """// Zero-Reflow Reviews Auto-slide
                const reviewsContainer = document.querySelector('.reviews-container');
                if (reviewsContainer) {
                    let autoScrollInterval;
                    let isUserInteracting = false;
                    let cachedCardWidth = 0;
                    let cachedMaxScroll = 0;
                    let isMobile = window.matchMedia('(max-width: 768px)').matches;

                    function updateReviewsMetrics() {
                        isMobile = window.matchMedia('(max-width: 768px)').matches;
                        if (!isMobile) return;
                        const card = reviewsContainer.querySelector(':scope > a');
                        if (card) {
                            cachedCardWidth = card.offsetWidth + 32;
                            cachedMaxScroll = reviewsContainer.scrollWidth - reviewsContainer.clientWidth - 10;
                        }
                    }

                    if ('requestIdleCallback' in window) {
                        requestIdleCallback(updateReviewsMetrics);
                    } else {
                        setTimeout(updateReviewsMetrics, 100);
                    }

                    let resizeTimer;
                    window.addEventListener('resize', () => {
                        clearTimeout(resizeTimer);
                        resizeTimer = setTimeout(updateReviewsMetrics, 200);
                    }, { passive: true });

                    function startAutoScroll() {
                        if (autoScrollInterval) clearInterval(autoScrollInterval);
                        autoScrollInterval = setInterval(() => {
                            if (!isMobile || isUserInteracting || !cachedCardWidth) return;
                            requestAnimationFrame(() => {
                                const currentScroll = reviewsContainer.scrollLeft;
                                const nextScroll = currentScroll + cachedCardWidth;
                                if (nextScroll >= cachedMaxScroll) {
                                    reviewsContainer.scrollTo({ left: 0, behavior: 'smooth' });
                                } else {
                                    reviewsContainer.scrollTo({ left: nextScroll, behavior: 'smooth' });
                                }
                            });
                        }, 4000);
                    }

                    if ('IntersectionObserver' in window) {
                        const observer = new IntersectionObserver((entries) => {
                            entries.forEach(entry => {
                                if (entry.isIntersecting) {
                                    updateReviewsMetrics();
                                    startAutoScroll();
                                } else {
                                    clearInterval(autoScrollInterval);
                                }
                            });
                        }, { threshold: 0.1 });
                        observer.observe(reviewsContainer);
                    } else {
                        startAutoScroll();
                    }

                    reviewsContainer.addEventListener('touchstart', () => {
                        isUserInteracting = true;
                        clearInterval(autoScrollInterval);
                    }, { passive: true });

                    reviewsContainer.addEventListener('touchend', () => {
                        isUserInteracting = false;
                        setTimeout(startAutoScroll, 2000);
                    }, { passive: true });
                }
            };

            """

if reviews_pattern.search(index_content):
    index_content = reviews_pattern.sub(optimized_reviews_script, index_content)
    print("Replaced reviews auto-slide script in index.html")

# Replace mousemove parallax script in index.html
parallax_pattern = re.compile(
    r'// Cached elements for puzzle tiles.*?(?=// Defer heavy or non-essential)',
    re.DOTALL
)

optimized_index_parallax = """// Zero-Reflow Throttled Mousemove Parallax
        let puzzleTiles = [];
        let mouseX = 0, mouseY = 0;
        let parallaxTicking = false;
        let halfWidth = window.innerWidth / 2;
        let halfHeight = window.innerHeight / 2;

        window.addEventListener('resize', () => {
            halfWidth = window.innerWidth / 2;
            halfHeight = window.innerHeight / 2;
        }, { passive: true });

        window.addEventListener('DOMContentLoaded', () => {
            puzzleTiles = Array.from(document.querySelectorAll('.puzzle-tile'));
        });

        document.addEventListener('mousemove', (e) => {
            mouseX = e.clientX;
            mouseY = e.clientY;

            if (!parallaxTicking && puzzleTiles.length > 0) {
                requestAnimationFrame(updateParallax);
                parallaxTicking = true;
            }
        }, { passive: true });

        function updateParallax() {
            const x = (halfWidth - mouseX) / 50;
            const y = (halfHeight - mouseY) / 50;

            for (let i = 0; i < puzzleTiles.length; i++) {
                const tile = puzzleTiles[i];
                const speed = parseFloat(tile.getAttribute('data-speed')) || 2;
                const xOffset = x * speed;
                const yOffset = y * speed;
                tile.style.transform = `translate3d(${xOffset}px, ${yOffset}px, 0) rotateX(${yOffset * 0.1}deg) rotateY(${xOffset * 0.1}deg)`;
            }

            parallaxTicking = false;
        }

        """

if parallax_pattern.search(index_content):
    index_content = parallax_pattern.sub(optimized_index_parallax, index_content)
    print("Replaced mousemove parallax in index.html")

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(index_content)


# 2. Optimize about.html
with open(about_path, 'r', encoding='utf-8') as f:
    about_content = f.read()

about_parallax_pattern = re.compile(
    r'// Parallax Mouse Logic.*?(?=// Lead Form Popup Logic)',
    re.DOTALL
)

optimized_about_parallax = """// Zero-Reflow Parallax Mouse Logic
    let aboutParallaxElements = [];
    let aboutParallaxTicking = false;
    let aboutMouseX = 0, aboutMouseY = 0;
    let aboutHalfWidth = window.innerWidth / 2;
    let aboutHalfHeight = window.innerHeight / 2;

    window.addEventListener('DOMContentLoaded', () => {
        aboutParallaxElements = Array.from(document.querySelectorAll('.parallax-element'));
    });

    window.addEventListener('resize', () => {
        aboutHalfWidth = window.innerWidth / 2;
        aboutHalfHeight = window.innerHeight / 2;
    }, { passive: true });

    document.addEventListener('mousemove', (e) => {
        aboutMouseX = e.clientX;
        aboutMouseY = e.clientY;

        if (!aboutParallaxTicking && aboutParallaxElements.length > 0) {
            requestAnimationFrame(updateAboutParallax);
            aboutParallaxTicking = true;
        }
    }, { passive: true });

    function updateAboutParallax() {
        const x = (aboutHalfWidth - aboutMouseX) / 100;
        const y = (aboutHalfHeight - aboutMouseY) / 100;

        for (let i = 0; i < aboutParallaxElements.length; i++) {
            const el = aboutParallaxElements[i];
            const speed = parseFloat(el.getAttribute('data-speed')) || 10;
            const xOffset = x * (speed / 10);
            const yOffset = y * (speed / 10);
            el.style.transform = `translate3d(${xOffset}px, ${yOffset}px, 0)`;
        }
        aboutParallaxTicking = false;
    }

    """

if about_parallax_pattern.search(about_content):
    about_content = about_parallax_pattern.sub(optimized_about_parallax, about_content)
    print("Replaced mousemove parallax in about.html")

with open(about_path, 'w', encoding='utf-8') as f:
    f.write(about_content)

print("Forced Reflow Optimization script executed successfully!")
