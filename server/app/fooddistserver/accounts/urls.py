from django.urls import path
from . import views

urlpatterns = [
    path('token/', views.token_exchange, name='token_exchange'),
]