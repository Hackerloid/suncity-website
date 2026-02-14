from django import forms
from website.models import BlogPost, Service

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['title', 'icon_class', 'tagline', 'offerings', 'why_it_matters', 'target_audience', 'order', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'icon_class': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'fas fa-shield-alt'}),
            'tagline': forms.TextInput(attrs={'class': 'form-control'}),
            'offerings': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'One item per line'}),
            'why_it_matters': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'target_audience': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'One item per line'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
