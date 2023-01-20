from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('total_funds_per_country/', views.total_funds_per_country, name='total_funds_per_country'),
    path('organisations/', views.organisations, name='organisations'),
    path('projects/', views.projects, name='projects'),
    path('', views.main, name='main'),
    path('projects/detail_project/<int:id>', views.detail_project, name='detail_project'),
    path('organisations/detail_organisation/<int:id>', views.detail_organisation, name='detail_organisation'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)