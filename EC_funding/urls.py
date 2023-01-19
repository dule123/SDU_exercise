from django.urls import path
from . import views

urlpatterns = [
    path('organisations/', views.organisations, name='organisations'),
    path('projects/', views.projects, name='projects'),
    path('', views.main, name='main'),
    path('EC_funding/', views.EC_funding, name='EC_funding'),
]