from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from .models import ContactSubmission

def index(request):
    return render(request, 'website/index.html')

def about(request):
    return render(request, 'website/about.html')

def services(request):
    return render(request, 'website/services.html')

def contact(request):
    success = False
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        ContactSubmission.objects.create(
            full_name=full_name,
            email=email,
            subject=subject,
            message=message
        )
        
        # Send Terminal Notification
        send_mail(
            subject=f"New Contact Inquiry: {subject}",
            message=f"Name: {full_name}\nEmail: {email}\n\nMessage:\n{message}",
            from_email=email,
            recipient_list=['admin@suncitytechnology.com'],
            fail_silently=False,
        )
        
        success = True
        
    return render(request, 'website/contact.html', {'success': success})
