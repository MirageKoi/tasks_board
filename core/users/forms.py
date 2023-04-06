from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

User = get_user_model()

class SignUpForm(UserCreationForm):
    password1 = forms.CharField(label=('Password'), widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label=('Password confirmation'), widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
        }


class SignInForm(AuthenticationForm):
    username = forms.CharField(label=('Username'), widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label=('Password'), widget=forms.PasswordInput(attrs={'class': 'form-control'}))
