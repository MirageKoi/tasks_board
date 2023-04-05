from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import redirect

from datetime import timedelta
from django.utils import timezone
from rest_framework.authtoken.models import Token

User = get_user_model()

class NonAdminSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user is an admin
        if request.user.is_authenticated and request.user.is_superuser:
            # If the user is an admin, use the default session settings
            response = self.get_response(request)
        else:
            # If the user is not an admin, check if they are authenticated
            if not request.user.is_authenticated:
                # If the user is not authenticated and not already on the login page, or is not API request, redirect to the login page
                if not (request.path == settings.LOGIN_URL or request.path == settings.REGISTER_URL or request.path.startswith('/api/')):
                    return redirect(settings.LOGIN_URL)
            else:
                # If the user is authenticated and not an admin, apply the custom session settings
                request.session.set_expiry(settings.NON_ADMIN_SESSION_EXPIRE_SECONDS)
                request.session.modified = True
            response = self.get_response(request)
        return response
    

class ExpiredTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')
            if last_activity and timezone.now() - last_activity > timezone.timedelta(minutes=1):
                # Refresh token
                Token.objects.filter(user=request.user).delete()
                Token.objects.create(user=request.user)
            request.session['last_activity'] = timezone.now()

        return response