from django import forms
from .models import Complaint

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        # These are the fields the citizen will fill out on the website
        fields = ['name', 'email', 'phone', 'category', 'location', 'description','image']
        
        # This adds styling boxes (Bootstrap classes) to make it look professional
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'yourname@example.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '10-digit Mobile Number'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Vastrapur, Satellite, Nikol'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe the issue or animal condition...'}),
            'Images':forms.FileInput(attrs={'class':'form-control'}),
        }