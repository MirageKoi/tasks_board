from django.urls import path
from users import views
from django.contrib.auth.views import LogoutView


app_name = "users"

urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("signin/", views.SignInView.as_view(), name="signin"),
    path("logout/", LogoutView.as_view(next_page="homepage"), name="logout")
]
