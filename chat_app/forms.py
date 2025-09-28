# Custom forms for clean UI
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class CleanUserCreationForm(UserCreationForm):
    """Clean registration form without Django's verbose help text"""
    
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': 'Username',
            'class': 'form-input'
        })
    )
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'class': 'form-input'
        })
    )
    
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm Password',
            'class': 'form-input'
        })
    )
    
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        
    # Override to remove help text
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove help text for all fields
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

class CleanLoginForm(forms.Form):
    """Clean login form with consistent styling"""
    
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Username',
            'class': 'form-input'
        })
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'class': 'form-input'
        })
    )
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if username and password:
            self.user_cache = authenticate(username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError("Invalid username or password.")
        return self.cleaned_data
    
    def get_user(self):
        return getattr(self, 'user_cache', None)
