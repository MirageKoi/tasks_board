from django.http import HttpRequest
from django.shortcuts import render
from django.views.generic import CreateView
from .forms import SignUpForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from rest_framework import generics
from .serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()
class SignUpView(CreateView):
    template_name = "signup.html"
    form_class = SignUpForm
    success_url = reverse_lazy("homepage")


class SignInView(LoginView):
    template_name = "signin.html"


class UserSignUpAPI(generics.CreateAPIView):
    # queryset = User.objects.all()
    serializer_class = UserSerializer
# from rest_framework.views import APIView
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response

# class MyView(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request, format=None):
#         content = {
#             'user': str(request.user),  # `django.contrib.auth.User` instance.
#             'auth': str(request.auth),  # `django.contrib.auth.Token` instance, если токен был предоставлен.
#         }
#         return Response(content)
