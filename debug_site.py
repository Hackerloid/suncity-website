import os
import django
import sys
import smtplib

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'suncity_project.settings')
try:
    django.setup()
except Exception as e:
    print(f"[FAIL] Django Setup: {e}")
    sys.exit(1)

from django.conf import settings
from django.db import connections
from django.db.utils import OperationalError

print("--- DIAGNOSTIC START ---")

# 1. Check Debug Mode
print(f"[INFO] DEBUG Mode: {settings.DEBUG}")

# 2. Check Database
try:
    db_conn = connections['default']
    db_conn.cursor()
    print("[PASS] Database Connection")
except OperationalError as e:
    print(f"[FAIL] Database Connection: {e}")

# 3. Check Email Configuration
print(f"[INFO] Email Host: {settings.EMAIL_HOST}")
print(f"[INFO] Email User: {settings.EMAIL_HOST_USER}")
if settings.EMAIL_HOST_PASSWORD == 'change-me-to-your-app-password':
    print("[WARN] Email Password is using default placeholder! This will fail.")
else:
    print("[INFO] Email Password is set (hidden)")

# 4. Test SMTP Connection
try:
    server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
    server.ehlo()
    if settings.EMAIL_USE_TLS:
        server.starttls()
    server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    print("[PASS] SMTP Authentication successful")
    server.quit()
except Exception as e:
    print(f"[FAIL] SMTP Connection: {e}")

print("--- DIAGNOSTIC END ---")
