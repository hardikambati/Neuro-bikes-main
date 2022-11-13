from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterUserAPIView.as_view()),
    path('login/', views.LoginUserAPIView.as_view()),

    path('user-details/', views.UserDetailAPIView.as_view()),
]