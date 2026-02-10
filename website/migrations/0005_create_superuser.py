from django.db import migrations
import os

def create_superuser(apps, schema_editor):
    # Get User model from the apps registry to ensure it's compatible with migrations
    User = apps.get_model('auth', 'User')
    
    username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'HACKERLOID')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'Let them cook @ 12.')
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@suncity.com')
    
    if username and password:
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)

class Migration(migrations.Migration):
    dependencies = [
        ('website', '0004_populate_services'),
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]
