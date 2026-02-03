document.addEventListener('DOMContentLoaded', () => {
    // Service Data Object
    const serviceDetails = {
        'cybersecurity': {
            title: 'Cybersecurity',
            icon: 'fa-shield-alt',
            tagline: 'Protecting your business from digital threats.',
            offer: [
                'Network security & firewall setup',
                'Endpoint protection (PCs, servers, devices)',
                'Penetration testing',
                'Vulnerability assessments',
                'Threat monitoring & incident response',
                'Security awareness training'
            ],
            why: 'Cyber attacks can shut down businesses, steal data, and damage reputation. We help you stay secure, compliant, and protected 24/7.',
            who: [
                'Businesses handling sensitive data',
                'Financial institutions',
                'Schools & organizations',
                'Companies with remote workers'
            ]
        },
        'it-support': {
            title: 'IT Support',
            icon: 'fa-headset',
            tagline: 'Keeping your systems running without interruption.',
            offer: [
                '24/7 technical support',
                'Hardware troubleshooting',
                'Software installation & support',
                'System upgrades',
                'Backup and recovery solutions',
                'Remote and on-site support'
            ],
            why: 'Downtime costs money. Our IT support ensures your operations run smoothly and efficiently.',
            who: [
                'Offices & corporate environments',
                'Small and medium businesses',
                'Organizations without in-house IT'
            ]
        },
        'networking': {
            title: 'Networking',
            icon: 'fa-network-wired',
            tagline: 'Building fast, secure, and reliable network systems.',
            offer: [
                'Network design & installation',
                'Router & switch configuration',
                'WiFi setup and optimization',
                'Server setup',
                'Network security implementation',
                'Maintenance and monitoring'
            ],
            why: 'A weak network slows productivity. We build high-performance, secure infrastructures.',
            who: [
                'Offices',
                'Schools',
                'Hospitals',
                'Growing businesses'
            ]
        },
        'software-development': {
            title: 'Software Development',
            icon: 'fa-code',
            tagline: 'Custom solutions built for your business needs.',
            offer: [
                'Web application development',
                'Mobile app development',
                'Business software systems',
                'Automation solutions',
                'System integration',
                'UI/UX design'
            ],
            why: 'Off-the-shelf software doesn’t always fit. We build tools tailored to your workflow.',
            who: [
                'Startups',
                'Companies with unique processes',
                'Businesses seeking automation'
            ]
        },
        // Placeholder for Web Development if needed later
        'web-development': {
            title: 'Web Development',
            icon: 'fa-laptop-code',
            tagline: 'Modern, responsive websites that grow your brand.',
            offer: [
                'Business websites',
                'E-commerce websites',
                'Portfolio websites',
                'Website redesign',
                'SEO optimization',
                'Website maintenance'
            ],
            why: 'Your website is your digital storefront. We ensure it attracts, converts, and represents your brand professionally.',
            who: [
                'Businesses',
                'Professionals',
                'Brands',
                'Organizations'
            ]
        },
        'cloud-solutions': {
            title: 'Cloud Solutions',
            icon: 'fa-cloud',
            tagline: 'Secure, scalable cloud infrastructure for your business.',
            offer: [
                'Cloud migration (AWS, Azure, GCP)',
                'Cloud security & configuration',
                'Hybrid cloud solutions',
                'SaaS implementation',
                'Cloud storage setup',
                'Infrastructure monitoring'
            ],
            why: 'The cloud offers unmatched flexibility. We ensure your transition is secure and your performance is optimized.',
            who: [
                'Businesses scaling rapidly',
                'Remote-first companies',
                'Enterprises reducing hardware costs'
            ]
        },
        'data-recovery': {
            title: 'Data Recovery',
            icon: 'fa-database',
            tagline: 'Protecting and restoring your most valuable assets.',
            offer: [
                'Automated backup systems',
                'Disaster recovery planning',
                'Hard drive data restoration',
                'Ransomware recovery support',
                'Cloud backup solutions',
                'Off-site data protection'
            ],
            why: 'Data loss can be catastrophic. We provide the safety nets and recovery expertise to keep you operational.',
            who: [
                'Businesses with critical databases',
                'Law firms and medical practices',
                'Finance-heavy organizations'
            ]
        },
        'system-integration': {
            title: 'System Integration',
            icon: 'fa-puzzle-piece',
            tagline: 'Connecting your tools for a seamless workflow.',
            offer: [
                'API development & integration',
                'Software-to-Software connectivity',
                'Unified communications setup',
                'Legacy system modernization',
                'Database synchronization',
                'Workflow automation'
            ],
            why: 'Disconnected systems cause friction. We unify your technology stack to improve efficiency and data accuracy.',
            who: [
                'Companies using multiple platforms',
                'Businesses scaling their operations',
                'Organizations seeking automation'
            ]
        },
        'it-consulting': {
            title: 'IT Consulting',
            icon: 'fa-chart-line',
            tagline: 'Strategic technology guidance for business growth.',
            offer: [
                'IT roadmap development',
                'Security & infrastructure audits',
                'Technology budget planning',
                'Digital transformation strategy',
                'Vendor selection support',
                'Compliance & risk management'
            ],
            why: 'Technology should be an investment, not just a cost. We help you make smart, strategic IT decisions.',
            who: [
                'Businesses undergoing growth',
                'Startups planning their tech stack',
                'Enterprises modernizing their systems'
            ]
        },
        'system-maintenance': {
            title: 'System Maintenance',
            icon: 'fa-tools',
            tagline: 'Proactive upkeep for peak performance.',
            offer: [
                'Daily system health checks',
                'Security patches & updates',
                'Hardware cleaning & maintenance',
                'Server optimization',
                'Performance tuning',
                'Asset management'
            ],
            why: 'Regular maintenance prevents expensive failures. We keep your systems running at their absolute best.',
            who: [
                'Offices with on-premise hardware',
                'Retailers with POS systems',
                'Operations requiring 100% uptime'
            ]
        }
    };

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
});
