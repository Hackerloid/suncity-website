import os
import django
import sys
from django.conf import settings

# Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'suncity_project.settings')
django.setup()

from django.core.mail import send_mail

def test_email():
    print("="*60)
    print(" SUNCITY EMAIL DIAGNOSTIC ")
    print("="*60)
    
    # 1. Check Configuration
    print(f"Backend:  {settings.EMAIL_BACKEND}")
    print(f"Host:     {settings.EMAIL_HOST}:{settings.EMAIL_PORT}")
    print(f"User:     {settings.EMAIL_HOST_USER}")
    print(f"TLS:      {settings.EMAIL_USE_TLS}")
    print(f"SSL:      {settings.EMAIL_USE_SSL}")
    
    # 2. Check Password
    pwd = settings.EMAIL_HOST_PASSWORD
    if not pwd or pwd == 'change-me-to-your-app-password':
        print("\n[!] EMAIL_HOST_PASSWORD is missing or default.")
        pwd = input("Enter your Gmail App Password: ").strip()
        # Inject into settings dynamically
        settings.EMAIL_HOST_PASSWORD = pwd
    else:
        print("Password: [Set]")

    # 3. Attempt Connection
    print("\nAttempting to send test email...")
    try:
        send_mail(
            subject='Suncity Local Diagnostic',
            message='If you receive this, your local configuration is CORRECT and the issue is strictly with Render networking.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.EMAIL_HOST_USER], # Send to yourself
            fail_silently=False,
        )
        print("\n✅ SUCCESS! Email sent successfully.")
        print("This proves your Code + Gmail Credentials + Custom Backend are ALL working.")
    except Exception as e:
        print(f"\n❌ FAILED. Error details:")
        print("-" * 30)
        import traceback
        traceback.print_exc()
        print("-" * 30)

if __name__ == "__main__":
    test_email()
