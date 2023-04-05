from django.urls import path
from users import views
from django.contrib.auth.views import LogoutView
from rest_framework.authtoken.views import obtain_auth_token


app_name = "users"

urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("signin/", views.SignInView.as_view(), name="signin"),
    path("logout/", LogoutView.as_view(next_page="homepage"), name="logout"),
    
]


urlpatterns += [
    path('api/token/', obtain_auth_token, name='token_auth'),
    path('api/signup/', views.UserSignUpAPI.as_view())

]