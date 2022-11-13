from django.urls import path
from . import views

urlpatterns = [
    path('buy/', views.UserTransactionView.as_view()),
    path('my-orders/', views.UserTransactionView.as_view()),

    path('cancel-order/', views.OrderCancellationView.as_view()),
    path('my-cancelled-orders/', views.OrderCancellationView.as_view()),
]