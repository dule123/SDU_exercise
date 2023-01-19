from django.contrib import admin
from EC_funding.models import Projects
from EC_funding.models import Organisations


class ProjectsAdmin(admin.ModelAdmin):
  list_display = ("acronym", "legalBasis", "status")

class OrganisationsAdmin(admin.ModelAdmin):
  list_display = ("name", "country",)

# Register your models here.
admin.site.register(Projects, ProjectsAdmin)
admin.site.register(Organisations, OrganisationsAdmin)

  
