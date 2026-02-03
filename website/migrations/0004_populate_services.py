from django.db import migrations

def populate_services(apps, schema_editor):
    Service = apps.get_model('website', 'Service')
    services = [
        {
            'title': 'Cybersecurity',
            'slug': 'cybersecurity',
            'icon_class': 'fa-shield-alt',
            'tagline': 'Protecting your business from digital threats.',
            'offerings': 'Network security & firewall setup\nEndpoint protection (PCs, servers, devices)\nPenetration testing\nVulnerability assessments\nThreat monitoring & incident response\nSecurity awareness training',
            'why_it_matters': 'Cyber attacks can shut down businesses, steal data, and damage reputation. We help you stay secure, compliant, and protected 24/7.',
            'target_audience': 'Businesses handling sensitive data\nFinancial institutions\nSchools & organizations\nCompanies with remote workers',
            'order': 1
        },
        {
            'title': 'Networking',
            'slug': 'networking',
            'icon_class': 'fa-network-wired',
            'tagline': 'Building fast, secure, and reliable network systems.',
            'offerings': 'Network design & installation\nRouter & switch configuration\nWiFi setup and optimization\nServer setup\nNetwork security implementation\nMaintenance and monitoring',
            'why_it_matters': 'A weak network slows productivity. We build high-performance, secure infrastructures.',
            'target_audience': 'Offices\nSchools\nHospitals\nGrowing businesses',
            'order': 2
        },
        {
            'title': 'IT Support',
            'slug': 'it-support',
            'icon_class': 'fa-headset',
            'tagline': 'Keeping your systems running without interruption.',
            'offerings': '24/7 technical support\nHardware troubleshooting\nSoftware installation & support\nSystem upgrades\nBackup and recovery solutions\nRemote and on-site support',
            'why_it_matters': 'Downtime costs money. Our IT support ensures your operations run smoothly and efficiently.',
            'target_audience': 'Offices & corporate environments\nSmall and medium businesses\nOrganizations without in-house IT',
            'order': 3
        },
        {
            'title': 'Software Development',
            'slug': 'software-development',
            'icon_class': 'fa-code',
            'tagline': 'Custom solutions built for your business needs.',
            'offerings': 'Web application development\nMobile app development\nBusiness software systems\nAutomation solutions\nSystem integration\nUI/UX design',
            'why_it_matters': 'Off-the-shelf software doesn’t always fit. We build tools tailored to your workflow.',
            'target_audience': 'Startups\nCompanies with unique processes\nBusinesses seeking automation',
            'order': 4
        }
    ]
    
    for s in services:
        Service.objects.get_or_create(slug=s['slug'], defaults=s)

class Migration(migrations.Migration):
    dependencies = [
        ('website', '0003_service'),
    ]

    operations = [
        migrations.RunPython(populate_services),
    ]
