document.addEventListener('DOMContentLoaded', () => {
    // Service Data Object - Fetch from dynamic script tag if available, else fallback
    let serviceDetails = {};
    const dataElement = document.getElementById('services-data');
    if (dataElement) {
        try {
            serviceDetails = JSON.parse(dataElement.textContent);
        } catch (e) {
            console.error('Error parsing service data:', e);
        }
    }

    // Modal Elements
    const modal = document.getElementById('service-modal');
    const modalTitle = document.getElementById('modal-title');
    const modalTagline = document.getElementById('modal-tagline');
    const modalOfferList = document.getElementById('modal-offer-list');
    const modalWhy = document.getElementById('modal-why');
    const modalWhoList = document.getElementById('modal-who-list');
    const modalIcon = document.getElementById('modal-icon');

    // Open Modal Function
    function openModal(serviceKey) {
        const data = serviceDetails[serviceKey];
        if (!data) return;

        // Populate Content
        modalTitle.textContent = data.title;
        modalTagline.textContent = data.tagline;
        modalWhy.textContent = data.why;
        
        // Update Icon
        modalIcon.className = `fas ${data.icon}`;

        // Populate Offer List
        modalOfferList.innerHTML = data.offer.map(item => `<li>${item}</li>`).join('');

        // Populate Who List
        modalWhoList.innerHTML = data.who.map(item => `<li>${item}</li>`).join('');

        // Show Modal
        modal.setAttribute('aria-hidden', 'false');
        document.body.style.overflow = 'hidden'; // Prevent scrolling
    }

    // Close Modal Function
    function closeModal() {
        modal.setAttribute('aria-hidden', 'true');
        document.body.style.overflow = ''; // Restore scrolling
    }

    // Event Listeners
    document.querySelectorAll('[data-service]').forEach(card => {
        card.addEventListener('click', () => {
            const serviceKey = card.getAttribute('data-service');
            openModal(serviceKey);
        });
    });

    // Close on click of close buttons or overlay
    document.querySelectorAll('[data-close]').forEach(el => {
        el.addEventListener('click', closeModal);
    });

    // Close on Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal.getAttribute('aria-hidden') === 'false') {
            closeModal();
        }
    });

    // --- Mobile Menu Logic ---
    const menuToggle = document.getElementById('mobile-menu-toggle');
    const navOverlay = document.getElementById('mobile-nav-overlay');
    const body = document.body;

    if (menuToggle && navOverlay) {
        menuToggle.addEventListener('click', () => {
            const isExpanded = menuToggle.getAttribute('aria-expanded') === 'true';
            
            // Toggle State
            menuToggle.setAttribute('aria-expanded', !isExpanded);
            navOverlay.classList.toggle('active');
            
            // Toggle Icon
            const icon = menuToggle.querySelector('i');
            if (icon) {
                icon.className = isExpanded ? 'fas fa-bars' : 'fas fa-times';
            }
            
            // Prevent Scroll when open
            body.style.overflow = isExpanded ? '' : 'hidden';
        });

        // Close when clicking a link
        navOverlay.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                menuToggle.setAttribute('aria-expanded', 'false');
                navOverlay.classList.remove('active');
                body.style.overflow = '';
                const icon = menuToggle.querySelector('i');
                if (icon) icon.className = 'fas fa-bars';
            });
        });
    }
});
