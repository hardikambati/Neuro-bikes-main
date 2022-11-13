from django.urls import path
from . import views

urlpatterns = [
    path('book-service/', views.BookServicing.as_view()),
    path('service-history/', views.BookServicing.as_view()),
]