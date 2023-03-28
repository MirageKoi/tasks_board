from django.http import HttpRequest
from django.shortcuts import render
from django.views.generic import CreateView
from .forms import SignUpForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy


class SignUpView(CreateView):
    template_name = "signup.html"
    form_class = SignUpForm
    success_url = reverse_lazy("homepage")


class SignInView(LoginView):
    template_name = "signin.html"
