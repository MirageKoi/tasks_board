from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from rest_framework import generics
from rest_framework import permissions

from .forms import SignInForm, SignUpForm
from .serializers import UserSerializer


class SignUpView(CreateView):
    template_name = "signup.html"
    form_class = SignUpForm
    success_url = reverse_lazy("homepage")


class SignInView(LoginView):
    template_name = "signin.html"
    form_class = SignInForm


class UserSignUpAPI(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
