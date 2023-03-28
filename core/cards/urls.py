from django.urls import path, include
from . import views


app_name = 'cards'

urlpatterns = [
    path('', views.CardListView.as_view(), name='cardlist'),
    path('<int:pk>', views.CardDetailView.as_view()),
    path('create/', views.CardCreateView.as_view())
]
