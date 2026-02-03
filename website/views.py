from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.conf import settings
from .models import ContactSubmission, BlogPost, Booking, Service
from .forms import BookingForm

def index(request):
    latest_posts = BlogPost.objects.order_by('-created_at')[:3]
    services = Service.objects.filter(is_active=True)[:4]
    return render(request, 'website/index.html', {
        'latest_posts': latest_posts,
        'services': services
    })

def about(request):
    return render(request, 'website/about.html')

def services(request):
    services = Service.objects.filter(is_active=True)
    return render(request, 'website/services.html', {'services': services})

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
            recipient_list=['suncitytechnology7@gmail.com'],
            fail_silently=False,
        )
        
        success = True
        
    return render(request, 'website/contact.html', {'success': success})

def blog_list(request):
    posts = BlogPost.objects.order_by('-created_at')
    return render(request, 'website/blog_list.html', {'posts': posts})

def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    return render(request, 'website/blog_detail.html', {'post': post})

def book_consultation(request):
    success = False
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save()
            
            # Send Notification
            send_mail(
                subject=f"New Consultation Booking: {booking.service}",
                message=f"Name: {booking.name}\nService: {booking.service}\nDate: {booking.date}\nTime: {booking.time}\n\nNotes:\n{booking.message}",
                from_email=booking.email,
                recipient_list=['suncitytechnology7@gmail.com'],
                fail_silently=False,
            )
            success = True
            return render(request, 'website/booking.html', {'success': success})
    else:
        form = BookingForm()
    
    return render(request, 'website/booking.html', {'form': form, 'success': success})
