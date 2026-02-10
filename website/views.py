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
        
        try:
            # 1. Email to Admin
            send_mail(
                subject="New Website Inquiry",
                message=f"Name: {full_name}\nEmail: {email}\nService Requested: {subject}\n\nMessage:\n{message}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )

            # 2. Email to Client
            send_mail(
                subject="We Received Your Request – SunCity Technology",
                message=f"Hi {full_name},\n\nThank you for reaching out! We have received your request regarding '{subject}'.\n\nOur team will review your message and get back to you shortly.\n\nBest regards,\nSunCity Technology Team",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Error sending email: {e}")
            # Ensure success is still True so the user sees the success page
            pass
        
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
            
            try:
                # 1. Email to Admin
                send_mail(
                    subject="New Consultation Booking",
                    message=f"Name: {booking.name}\nEmail: {booking.email}\nPhone: {booking.phone}\nService: {booking.service}\nDate: {booking.date}\nTime: {booking.time}\n\nNotes:\n{booking.message}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.EMAIL_HOST_USER],
                    fail_silently=False,
                )

                # 2. Email to Client
                send_mail(
                    subject="Consultation Request Received – SunCity Technology",
                    message=f"Hi {booking.name},\n\nWe have received your request for a Consultation on '{booking.service}'.\n\nDate: {booking.date}\nTime: {booking.time}\n\nOur team will confirm your appointment shortly.\n\nBest regards,\nSunCity Technology Team",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[booking.email],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Error sending email: {e}")
                pass

            success = True
            return render(request, 'website/booking.html', {'success': success})
    else:
        form = BookingForm()
    
    return render(request, 'website/booking.html', {'form': form, 'success': success})
