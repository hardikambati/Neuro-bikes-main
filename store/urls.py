from django.urls import path
from . import views

urlpatterns = [
    path('add-bike/', views.StaffAccessView.as_view()),
    path('all-bikes/', views.BikeListView.as_view()),
]