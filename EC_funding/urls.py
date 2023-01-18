from django.urls import path
from . import views

urlpatterns = [
    path('EC_funding/', views.EC_funding, name='EC_funding'),
]