from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.http import HttpResponse # Temporary for debug
import traceback

def dashboard_login(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_staff:
                    login(request, user)
                    return redirect('dashboard_home')
                else:
                    messages.error(request, "Access denied. Admin privileges required.")
            else:
                messages.error(request, "Invalid username or password.")
        return render(request, 'dashboard/login.html')
    except Exception as e:
        return HttpResponse(f"<h1>Dashboard Error</h1><p>{e}</p><pre>{traceback.format_exc()}</pre>", status=500)

def dashboard_logout(request):
    logout(request)
    return redirect('dashboard_login')

from website.models import ContactSubmission, Booking, BlogPost, Service

@login_required
def dashboard_home(request):
    if not request.user.is_staff:
        messages.error(request, "Access denied.")
        return redirect('home')
        
    context = {
        'page_title': 'Dashboard Overview',
        'new_messages_count': ContactSubmission.objects.filter(status='new').count(),
        'pending_bookings_count': Booking.objects.filter(status='pending').count(),
        'services_count': Service.objects.count(),
        'services_count': Service.objects.count(),
        'blog_posts_count': BlogPost.objects.count(),
    }
    return render(request, 'dashboard/home.html', context)

from django.shortcuts import get_object_or_404

@login_required
def contact_list(request):
    if not request.user.is_staff:
        return redirect('home')
        
    contacts = ContactSubmission.objects.all().order_by('-created_at')
    return render(request, 'dashboard/contact_list.html', {'contacts': contacts})

@login_required
def contact_detail(request, pk):
    if not request.user.is_staff:
        return redirect('home')
        
    contact = get_object_or_404(ContactSubmission, pk=pk)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status:
            contact.status = new_status
            contact.save()
            messages.success(request, f"Status updated to '{contact.get_status_display()}'")
            return redirect('contact_detail', pk=pk)
            
    return render(request, 'dashboard/contact_detail.html', {'contact': contact})

@login_required
def contact_delete(request, pk):
    if not request.user.is_staff:
        return redirect('home')
        
    contact = get_object_or_404(ContactSubmission, pk=pk)
    if request.method == 'POST':
        contact.delete()
        messages.success(request, "Message deleted successfully.")
        return redirect('contact_list')
    return redirect('contact_list')

@login_required
def booking_list(request):
    if not request.user.is_staff:
        return redirect('home')
        
    bookings = Booking.objects.all().order_by('-created_at')
    return render(request, 'dashboard/booking_list.html', {'bookings': bookings})

@login_required
def booking_detail(request, pk):
    if not request.user.is_staff:
        return redirect('home')
        
    booking = get_object_or_404(Booking, pk=pk)
    
    if request.method == 'POST':
        update_type = request.POST.get('update_type')
        
        if update_type == 'status':
            new_status = request.POST.get('status')
            if new_status:
                booking.status = new_status
                booking.save()
                messages.success(request, f"Booking status updated to '{booking.get_status_display()}'")
        
        elif update_type == 'workflow':
            new_workflow = request.POST.get('workflow_status')
            if new_workflow:
                booking.workflow_status = new_workflow
                booking.save()
                messages.success(request, f"Workflow status updated to '{booking.get_workflow_status_display()}'")

        return redirect('booking_detail', pk=pk)
            
    return render(request, 'dashboard/booking_detail.html', {'booking': booking})

from .forms import BlogPostForm, ServiceForm

# --- Blog Management ---
@login_required
def blog_list(request):
    if not request.user.is_staff:
        return redirect('home')
    posts = BlogPost.objects.all().order_by('-created_at')
    return render(request, 'dashboard/blog_list.html', {'posts': posts})

@login_required
def blog_create(request):
    if not request.user.is_staff:
        return redirect('home')
    
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Blog post created successfully.")
            return redirect('blog_list')
    else:
        form = BlogPostForm()
    return render(request, 'dashboard/blog_form.html', {'form': form, 'title': 'Create Blog Post'})

@login_required
def blog_edit(request, pk):
    if not request.user.is_staff:
        return redirect('home')
    
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Blog post updated successfully.")
            return redirect('blog_list')
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'dashboard/blog_form.html', {'form': form, 'title': 'Edit Blog Post'})

@login_required
def blog_delete(request, pk):
    if not request.user.is_staff:
        return redirect('home')
    
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        post.delete()
        messages.success(request, "Blog post deleted.")
    return redirect('blog_list')

# --- Service Management ---
@login_required
def service_list(request):
    if not request.user.is_staff:
        return redirect('home')
    services = Service.objects.all().order_by('order')
    return render(request, 'dashboard/service_list.html', {'services': services})

@login_required
def service_create(request):
    if not request.user.is_staff:
        return redirect('home')
    
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Service created successfully.")
            return redirect('service_list')
    else:
        form = ServiceForm()
    return render(request, 'dashboard/service_form.html', {'form': form, 'title': 'Create New Service'})

@login_required
def service_edit(request, pk):
    if not request.user.is_staff:
        return redirect('home')
    
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, "Service updated successfully.")
            return redirect('service_list')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'dashboard/service_form.html', {'form': form, 'title': 'Edit Service'})

@login_required
def service_delete(request, pk):
    if not request.user.is_staff:
        return redirect('home')
    
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        service.delete()
        messages.success(request, "Service deleted.")
    return redirect('service_list')
