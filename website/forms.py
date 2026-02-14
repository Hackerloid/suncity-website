from django import forms
from .models import Booking, Service

class BookingForm(forms.ModelForm):
    service = forms.ChoiceField(
        choices=[('', 'Select a Service')],
        widget=forms.Select(attrs={'class': 'form-input'})
    )

    class Meta:
        model = Booking
        fields = ['name', 'email', 'phone', 'service', 'date', 'time', 'message']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-input'}),
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'john@example.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '+233 ...'}),
            'message': forms.Textarea(attrs={'class': 'form-input', 'rows': 4, 'placeholder': 'Any specific details?'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Fetch active services from the database
        services = Service.objects.filter(is_active=True).order_by('order', 'title')
        dynamic_choices = [('', 'Select a Service')] + [(s.slug, s.title) for s in services]
        self.fields['service'].choices = dynamic_choices
