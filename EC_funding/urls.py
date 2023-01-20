from django.urls import path
from . import views

urlpatterns = [
    path('total_funds_per_country/', views.total_funds_per_country, name='total_funds_per_country'),
    path('organisations/', views.organisations, name='organisations'),
    path('projects/', views.projects, name='projects'),
    path('', views.main, name='main'),
]