from django.contrib import admin
from .models import ContactSubmission

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'subject', 'created_at')
    readonly_fields = ('full_name', 'email', 'subject', 'message', 'created_at')
    search_fields = ('full_name', 'email', 'subject')
    list_filter = ('created_at',)
    
    def has_add_permission(self, request):
        return False
