from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

class SignUpForm(UserCreationForm):
    
    email = forms.CharField(widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email')