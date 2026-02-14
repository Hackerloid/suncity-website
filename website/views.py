from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from .models import ContactSubmission, BlogPost, Booking, Service
from .forms import BookingForm
import logging

logger = logging.getLogger(__name__)

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
    error_message = None
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        try:
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
                logger.error(f"Error sending email: {e}", exc_info=True)
                # Don't fail the form if email fails, just log it
                pass
            
            success = True
        except Exception as e:
            logger.error(f"Error saving contact submission: {e}", exc_info=True)
            error_message = f"Contact Error: {e}"
        
    return render(request, 'website/contact.html', {'success': success, 'error_message': error_message})

def blog_list(request):
    posts = BlogPost.objects.order_by('-created_at')
    return render(request, 'website/blog_list.html', {'posts': posts})

def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    return render(request, 'website/blog_detail.html', {'post': post})

def book_consultation(request):
    success = False
    error_message = None
    form = None
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            try:
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
                    logger.error(f"Error sending email: {e}", exc_info=True)
                    # Don't fail the form if email fails, just log it
                    pass

                success = True
                return render(request, 'website/booking.html', {'success': success})
            except Exception as e:
                logger.error(f"Error saving booking: {e}", exc_info=True)
                error_message = f"Booking Error: {e}"
        else:
            # Debugging: Show specific errors
            error_details = []
            for field, errors in form.errors.items():
                error_details.append(f"{field}: {', '.join(errors)}")
            error_message = f"Please check the form: {'; '.join(error_details)}"
    else:
        form = BookingForm()
    
    return render(request, 'website/booking.html', {'form': form, 'success': success, 'error_message': error_message})

def test_db(request):
    results = []
    
    # 1. Database Test
    try:
        from .models import ContactSubmission
        # Create
        c = ContactSubmission.objects.create(
            full_name="Diagnostic Test",
            email="test@suncity.com",
            subject="Test",
            message="Testing DB"
        )
        # Delete
        c.delete()
        results.append("✅ Database Write/Delete: SUCCESS")
    except Exception as e:
        import traceback
        logger.error(f"Database Test Failed: {e}", exc_info=True)
        results.append(f"❌ Database Error: {e}<br><pre>{traceback.format_exc()}</pre>")

    # 2. Email Test
    try:
        send_mail(
            subject="Diagnostic Email Test",
            message="If you received this, email sending is working.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.EMAIL_HOST_USER],
            fail_silently=False,
        )
        results.append("✅ Email Sending: SUCCESS")
    except Exception as e:
        import traceback
        logger.error(f"Email Test Failed: {e}", exc_info=True)
        results.append(f"❌ Email Error: {e}<br><pre>{traceback.format_exc()}</pre>")
        
    return HttpResponse("<br>".join(results))
