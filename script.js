document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const dateTimeElement = document.getElementById('current-date-time');
    const homeView = document.getElementById('home-view');
    const articleView = document.getElementById('article-view');
    const siteLogo = document.getElementById('site-logo');
    const navLinks = document.querySelectorAll('#main-nav a');
    
    // Article Detail Elements
    const artTitle = document.getElementById('art-title');
    const artCategory = document.getElementById('art-category');
    const artImage = document.getElementById('art-image');
    const artMeta = document.getElementById('art-meta');
    const artBody = document.getElementById('art-body');

    // Article content database
    const articles = {
        // Index/Home articles
        'deep-blue': {
            title: 'The Deep Blue Mystery: A Journey to the Uncharted Abyssal Zones',
            category: 'EXPLORATION',
            image: 'hero_ocean_cinematic_1777952019449.png',
            meta: 'By Julian Reed | May 5, 2026 | 15 min read',
            lead: 'The ocean covers more than 70% of our planet\'s surface, yet over 80% of it remains unmapped, unobserved, and unexplored.',
            body: `<p>Recently, a team of international oceanographers embarked on a 3-month expedition into the Philippine Sea. What they found was not just a desolate wasteland of sand and rock, but a vibrant, albeit alien, ecosystem powered by hydrothermal vents and chemical energy rather than sunlight.</p>
                    
                    <h3>The Bioluminescent Frontier</h3>
                    <p>As our submersible descended past 4,000 meters into the "Abyssal Zone," the world outside the reinforced acrylic dome turned into a dance of phantom lights. Species of jellyfish that resemble floating chandeliers pulsed with electric blues and violets. We encountered a new species of Siphonophore—a colonial organism that can reach lengths of over 40 meters, making it potentially the longest animal on Earth.</p>
                    
                    <blockquote>"We aren't just looking at new species; we are looking at a new way to live. The pressure here is enough to crush a luxury car, yet these creatures move with a grace that is almost haunting." — Dr. Elena Vance</blockquote>

                    <p>The significance of these findings extends beyond mere curiosity. The microbes found near these volcanic vents are being studied for potential breakthroughs in medical science, specifically in the treatment of extreme viral infections.</p>`
        },
        'culinary-secrets': {
            title: 'Culinary Excellence: 5 Secret Seafood Recipes from Remote Coastal Villages',
            category: 'CULINARY',
            image: 'seafood_platter_magazine_1777952036710.png',
            meta: 'By Maria Santos | Dec 9, 2026 | 8 min read',
            lead: 'From the salt-crusted techniques of the Mediterranean to the spicy, aromatic broths of Southeast Asia, discover recipes passed down through generations.',
            body: `<p>In the remote fishing villages of southern Portugal, grandmother Maria has been preparing the same cataplana dish for over 60 years. The secret, she says, is patience and the freshest catch of the day.</p>
                    
                    <h3>1. Cataplana de Marisco</h3>
                    <p>This traditional Portuguese seafood stew combines clams, mussels, shrimp, and white fish in a harmonious blend of tomatoes, peppers, onions, and white wine. The dish is traditionally cooked in a cataplana pot, which seals in steam and all the aromatic flavors.</p>
                    
                    <h3>2. Thai Tom Yum Goong</h3>
                    <p>The famous Thai soup that balances sour, spicy, and savory flavors in a single bowl. Fresh prawns, lemongrass, galangal, kaffir lime leaves, and mushrooms create an unforgettable experience.</p>`
        },
        'hidden-gems': {
            title: 'The "Hidden Gems" of the World\'s Coastlines You\'ve Never Heard Of',
            category: 'TRAVEL',
            image: 'coastal_hidden_gem_1777952070037.png',
            meta: 'By Elena Martinez | Dec 7, 2026 | 12 min read',
            lead: 'Escape the crowds and discover the secluded turquoise bays that remain untouched by modern tourism.',
            body: `<p>Beyond the Instagram-famous beaches and tourist-trapped coastlines lies a world of pristine shores, hidden coves, and forgotten fishing villages waiting to be explored.</p>
                    
                    <h3>The Azores: Europe\'s Best-Kept Secret</h3>
                    <p>This Portuguese archipelago in the North Atlantic offers dramatic volcanic landscapes, whale watching, and hot springs—all without the crowds of more popular destinations.</p>
                    
                    <h3>Palawan, Philippines</h3>
                    <p>Often called the "Last Frontier of the Philippines," Palawan features the iconic El Nido and Coron, with their dramatic limestone cliffs and crystal-clear lagoons.</p>`
        },
        'future-fishing': {
            title: 'The Future of Fishing: Can AI Help Restore Our Ocean\'s Fish Populations?',
            category: 'ENVIRONMENT',
            image: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSXiThj5u97SNGgWCV2Hf8HhpKmuENp-U7A_g&s',
            meta: 'By Dr. Marine Chen | Dec 5, 2026 | 6 min read',
            lead: 'New AI-powered monitoring systems are revolutionizing sustainable fishing practices worldwide.',
            body: `<p>Artificial intelligence is transforming how we manage our oceans. From satellite tracking of fishing vessels to machine learning algorithms that predict fish migration patterns, technology offers new hope for depleted fish stocks.</p>
                    
                    <h3>Smart Fishing Nets</h3>
                    <p>New "smart" fishing nets equipped with sensors can distinguish between target species and bycatch, automatically adjusting to release unwanted species unharmed.</p>`
        },
        'great-barrier-reef': {
            title: 'The Great Barrier Reef\'s Surprising Recovery in Northern Sectors',
            category: 'ENVIRONMENT',
            image: 'https://i.guim.co.uk/img/media/7dc395c8d08f2efba36b3b4adeed913bd917cf91/0_153_2045_1227/master/2045.jpg?width=1200&quality=85&auto=format&fit=max&s=d871f3c3561112cb6b5068afae5a76a7',
            meta: 'By Dr. James Morrison | Nov 30, 2026 | 8 min read',
            lead: 'Despite decades of decline, scientists are witnessing unexpected regeneration in Australia\'s iconic reef system.',
            body: `<p>In a remarkable turn of events, marine biologists have documented significant coral recovery in the northern sections of the Great Barrier Reef. After years of devastating bleaching events, the resilient ecosystem is showing signs of renewal.</p>
                    
                    <h3>A Beacon of Hope</h3>
                    <p>Researchers from the Australian Institute of Marine Science report that coral cover in some northern sections has increased by up to 30% over the past two years, with diverse species returning to areas previously devastated by bleaching.</p>
                    
                    <h3>What\'s Driving the Recovery?</h3>
                    <p>Cooler water temperatures, reduced crown-of-thorns starfish outbreaks, and improved water quality have contributed to the unexpected recovery, offering a glimmer of hope for one of the world\'s most iconic natural wonders.</p>`
        },
        'fishing-traditions': {
            title: 'Ancient Fishing Traditions That Still Survive Today',
            category: 'CULTURE',
            image: 'https://images.unsplash.com/photo-1535025183041-0991a977e25b?w=800',
            meta: 'By Arthur Grant | Dec 3, 2026 | 10 min read',
            lead: 'From the wooden dhoni boats of the Maldives to the fish traps of Portugal\'s Algarve coast.',
            body: `<p>In an age of industrial fishing and factory ships, traditional fishing methods are disappearing. But in some corners of the world, ancient techniques survive—carried forward by practitioners who see them as more than just ways to catch fish.</p>
                    
                    <h3>The Coracles of Wales</h3>
                    <p>These lightweight, egg-shaped boats have been used for river fishing in Wales for over 2,000 years. Made from animal skins stretched over wooden frames, coracles require extraordinary skill to master.</p>`
        },
        'travel-1': {
            title: 'Yasawa Islands, Fiji: The Ultimate Tropical Escape',
            category: 'TRAVEL',
            image: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTihOag4VrlS4K3j34KllHOhlqC9PXGVXVtkw&s',
            meta: 'By Elena Martinez | Dec 1, 2026 | 12 min read',
            lead: 'Escape to Fiji\'s most breathtaking island chain, where turquoise waters meet dramatic volcanic peaks.',
            body: `<p>The Yasawa Islands are a chain of volcanic islands in Fiji, known for their stunning natural beauty, traditional villages, and some of the world's best diving and snorkeling spots.</p>
                    
                    <h3>Getting There</h3>
                    <p>Reachable only by boat from Denarau Marina, the journey itself is part of the adventure. The catamaran ride offers panoramic views of the Blue Lagoon, made famous by the 1980 film of the same name.</p>
                    
                    <h3>What to Expect</h3>
                    <p>With limited development and no roads between islands, the Yasawas offer an authentic Fijian experience. Village visits, traditional lovo feasts, and starlit beaches await those seeking true escape.</p>`
        },
        'culinary-1': {
            title: 'Wild vs. Farmed Salmon: The Great Debate',
            category: 'CULINARY',
            image: 'https://i.ytimg.com/vi/_5JwOONcyrE/sddefault.jpg',
            meta: 'By Chef Marcus Webb | Nov 28, 2026 | 10 min read',
            lead: 'Understanding the differences between wild-caught and farmed salmon for your health and the environment.',
            body: `<p>The salmon on your plate likely came from one of two sources: the wild, where fish swim freely in cold ocean waters, or from farms, where millions are raised in crowded net pens. The choice between them involves taste, nutrition, sustainability, and ethics.</p>
                    
                    <h3>Wild Salmon</h3>
                    <p>Wild-caught salmon get their distinctive pink-orange color from a natural diet of crustaceans and small fish. They are leaner and have a more complex, robust flavor. Nutritionally, wild salmon is higher in minerals and typically lower in fat.</p>
                    
                    <h3>Farmed Salmon</h3>
                    <p>Farmed salmon is fed pellets that include synthetic pigments to achieve the same color as wild fish. While farm-raised salmon tends to be fattier and more marbled, critics point to concerns about antibiotics, pollution of local ecosystems, and escape of farmed fish into wild populations.</p>`
        },
        'oyster-appreciation': {
            title: 'The Art of Oyster Appreciation',
            category: 'CULINARY',
            image: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSM6eRmfl-Jk6A9ydphMrKA2jsTcN937FT8DA&s',
            meta: 'By Sophie Laurent | Nov 25, 2026 | 8 min read',
            lead: 'A beginner\'s guide to understanding and enjoying different oyster varieties from around the world.',
            body: `<p>Oysters have been prized since ancient times for their unique taste and alleged aphrodisiac properties. Today, understanding oysters is a culinary journey that spans continents and flavors.</p>
                    
                    <h3>Pacific vs. Atlantic</h3>
                    <p>Pacific oysters (Crassostrea gigas) have a more complex, fruity flavor with a hints of melon and cucumber. Atlantic oysters (Crassostrea virginica) tend to be brinier and more metallic, with a smoother finish.</p>
                    
                    <h3>How to Taste</h3>
                    <p>The traditional way: lift the oyster to your lips, tip it back, and let the liquor flood your palate. Chew gently to experience the full range of flavors before swallowing. Many enthusiasts say the briny "ocean" taste should hit first, followed by sweetness, then a clean finish.</p>`
        },
        'environment-1': {
            title: 'The Ocean Plastic Crisis: 2026 Status Update - Are We Winning or Losing?',
            category: 'ENVIRONMENT',
            image: 'https://images.unsplash.com/photo-1583212292454-1fe6229603b7?w=1200',
            meta: 'By Dr. Marine Chen | Nov 28, 2026 | 18 min read',
            lead: 'Five years after the ambitious Global Ocean Cleanup initiative began, we assess what actually works.',
            body: `<p>The Great Pacific Garbage Patch, spanning 1.6 million square kilometers, has been the target of countless cleanup efforts. But the problem is far larger than any single initiative can address.</p>`
        },
        'people-1': {
            title: 'A Life on the Waves: The quiet resilience of Ha Long Bay\'s elders',
            category: 'PEOPLE',
            image: 'traditional_fisherman_portrait_1777952054951.png',
            meta: 'By Nguyen Van Minh | Nov 25, 2026 | 15 min read',
            lead: 'Mr. Sau has spent 40 years on a wooden boat, facing storms and solitude to raise a family.',
            body: `<p>In the misty waters of Ha Long Bay, where limestone karsts rise dramatically from the sea, an older generation of fishermen continues traditions that predate Vietnam\'s modern era.</p>`
        },
        'culture-1': {
            title: 'Lighthouses of the Atlantic: Sentinels of the Sea',
            category: 'CULTURE',
            image: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQC3u_z3EVPvHjvWNz3IoIvqaNNS-2xXD75Iw&s',
            meta: 'By Robert McAllister | Nov 22, 2026 | 12 min read',
            lead: 'The history and preservation efforts of America\'s iconic coastal lighthouses.',
            body: `<p>For centuries, lighthouses have stood as silent guardians along our coastlines, guiding sailors through treacherous waters and warning them of dangerous shoals. These iconic structures embody a romantic era of maritime history that continues to captivate our imagination.</p>
                    
                    <h3>Boston Light</h3>
                    <p>America's oldest operational lighthouse, built in 1716, has guided vessels into Boston Harbor for over three centuries. Today, it remains an active aid to navigation while serving as a living museum of maritime heritage.</p>
                    
                    <h3>Cape Hatteras Light</h3>
                    <p>The tallest brick lighthouse in the United States, standing 207 feet, Cape Hatteras Light has been protecting ships from the infamous "Graveyard of the Atlantic" since 1870.</p>`
        },
        'opinion-1': {
            title: 'Sustainable Seafood: Why this is the only path to saving our oceans',
            category: 'OPINION',
            image: 'https://images.unsplash.com/photo-1510414842594-a61c69b5ae57?w=1200',
            meta: 'By Dr. Sarah Thompson | Nov 20, 2026 | 8 min read',
            lead: 'The choices we make at the dinner table have far-reaching consequences for ocean health.',
            body: `<p>Every piece of fish we consume represents a choice—a choice that either supports sustainable practices or contributes to the collapse of marine ecosystems.</p>`
        }
    };

    // Update date and time
    function updateDateTime() {
        const now = new Date();
        const options = { day: 'numeric', month: 'long', year: 'numeric' };
        const dateStr = now.toLocaleDateString('en-US', options);
        const timeStr = now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: true });
        if (dateTimeElement) dateTimeElement.textContent = `${dateStr} | ${timeStr}`;
    }
    updateDateTime();
    setInterval(updateDateTime, 60000);

    // Navigation Logic
    function showHome() {
        if (homeView) homeView.classList.remove('hidden');
        if (articleView) articleView.classList.add('hidden');
        window.scrollTo(0, 0);
        navLinks.forEach(link => link.classList.remove('active'));
        const homeLink = document.querySelector('[data-view="home"]');
        if (homeLink) homeLink.classList.add('active');
    }

    function showArticle(articleId) {
        const article = articles[articleId];
        const mainContent = document.querySelector('main');
        
        // Hide main content and show article view
        if (mainContent) mainContent.classList.add('hidden');
        if (articleView) articleView.classList.remove('hidden');
        window.scrollTo(0, 0);
        
        if (article && artTitle) {
            artTitle.textContent = article.title;
            artCategory.textContent = article.category;
            artImage.src = article.image;
            artImage.alt = article.title;
            if (artMeta) artMeta.textContent = article.meta;
            if (artBody) {
                artBody.innerHTML = `
                    <p class="lead">${article.lead}</p>
                    ${article.body}
                `;
            }
        }
    }

    // Back to list button functionality
    function setupBackButton() {
        const articleDetail = document.querySelector('.article-detail');
        if (articleDetail && !articleDetail.querySelector('.back-btn')) {
            const backBtn = document.createElement('button');
            backBtn.className = 'back-btn';
            backBtn.innerHTML = '← Back to Articles';
            backBtn.style.cssText = 'margin-bottom: 20px; padding: 10px 20px; background: var(--gray-light); border: 1px solid var(--border-color); cursor: pointer; font-size: 0.9rem;';
            backBtn.addEventListener('click', () => {
                if (articleView) articleView.classList.add('hidden');
                const mainContent = document.querySelector('main');
                if (mainContent) mainContent.classList.remove('hidden');
                window.scrollTo(0, 0);
            });
            articleDetail.insertBefore(backBtn, articleDetail.firstChild);
        }
    }

    // Event Listeners
    if (siteLogo) {
        siteLogo.addEventListener('click', (e) => {
            e.preventDefault();
            showHome();
        });
    }
    
    document.querySelectorAll('.read-article').forEach(trigger => {
        trigger.addEventListener('click', (e) => {
            e.preventDefault();
            const id = trigger.getAttribute('data-article');
            showArticle(id);
        });
    });

    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            const view = link.getAttribute('data-view');
            
            if (view === 'home') {
                e.preventDefault();
                showHome();
            }
        });
    });

    // Comment Form
    function setupCommentForm() {
        document.querySelectorAll('.comment-form').forEach(form => {
            form.addEventListener('submit', (e) => {
                e.preventDefault();
                const name = form.querySelector('input').value;
                const text = form.querySelector('textarea').value;
                
                const commentList = form.closest('.add-comment')?.previousElementSibling;
                if (commentList) {
                    const newComment = document.createElement('div');
                    newComment.className = 'comment';
                    newComment.innerHTML = `
                        <div class="comment-header">
                            <span class="username">${name}</span>
                            <span class="date">Just now</span>
                        </div>
                        <p class="comment-text">${text}</p>
                    `;
                    
                    commentList.appendChild(newComment);
                    form.reset();
                    alert('Thank you for your comment!');
                }
            });
        });
    }
    setupCommentForm();

    // Region Tabs (for Travel page)
    const regionTabs = document.querySelectorAll('.region-tab');
    regionTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const region = tab.getAttribute('data-region');
            
            regionTabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            
            document.querySelectorAll('.region-content').forEach(content => {
                content.classList.remove('active');
            });
            
            const selectedContent = document.getElementById(region);
            if (selectedContent) {
                selectedContent.classList.add('active');
            }
        });
    });

    // Recipe Tabs (for Culinary page)
    const recipeTabs = document.querySelectorAll('.recipe-tab');
    recipeTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            recipeTabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
        });
    });

    // Reveal animations
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.news-item, .opinion-item, .story-card, .person-card, .featured-main, .destination-card, .recipe-card, .experience-card, .region-card, .mpa-card, .research-card, .project-card, .sustainable-card, .species-card, .profile-card, .scientist-card, .community-card, .essay-card, .craft-card, .myth-card, .festival-card, .book-card, .arch-card, .editorial-card, .expert-card, .debate-card, .letter-card, .analysis-card, .media-card, .guest-card, .tip-card, .technique-card, .cuisine-card, .review-card, .luxury-card, .env-card, .haenyeo-feature, .rising-card, .climate-card, .zone-card, .threat-card, .secret-item, .craft-item, .climate-stat, .issue-card, .generation-item, .art-period').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'all 0.6s ease-out';
        observer.observe(el);
    });

    // Newsletter Form
    document.querySelectorAll('#subscribe-form').forEach(subscribeForm => {
        subscribeForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const email = subscribeForm.querySelector('input[type="email"]').value;
            if (email) {
                alert('Thank you for subscribing to Ocean & Seafood!');
                subscribeForm.reset();
            }
        });
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href !== '#') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth'
                    });
                }
            }
        });
    });

    // Play button click (for video cards)
    document.querySelectorAll('.play-button').forEach(button => {
        button.addEventListener('click', () => {
            alert('Video player would open here');
        });
    });

    // Setup back button when article view exists
    setupBackButton();
});
