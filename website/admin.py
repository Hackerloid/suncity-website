from django.contrib import admin
from .models import ContactSubmission, BlogPost, Booking, Service

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'tagline')

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'subject', 'created_at')
    readonly_fields = ('full_name', 'email', 'subject', 'message', 'created_at')
    search_fields = ('full_name', 'email', 'subject')
    list_filter = ('created_at',)
    
    def has_add_permission(self, request):
        return False

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'content')
    list_filter = ('created_at', 'author')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'service', 'date', 'time', 'status')
    list_filter = ('status', 'service', 'date', 'created_at')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Customer Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Booking Details', {
            'fields': ('service', 'date', 'time', 'status', 'created_at')
        }),
        ('Additional Information', {
            'fields': ('message',)
        }),
    )
