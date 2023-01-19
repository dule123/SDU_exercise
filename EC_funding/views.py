from django.http import HttpResponse
from django.template import loader
from .models import Organisations
from .models import Projects
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage
from django.shortcuts import render

def EC_funding(request):
  template = loader.get_template('start.html')
  return HttpResponse(template.render())

def main(request):
  template = loader.get_template('main.html')
  return HttpResponse(template.render())

def organisations(request):

    # select onlt the unique organisations, based on the organisationID
    myorganisations = Organisations.objects.distinct('organisationID').all().values()

    # use paginator to display 100 organisations at the time 
    paginator = Paginator(myorganisations, 100)
    page = request.GET.get('page')
    try:
        organisations = paginator.page(page)
    except PageNotAnInteger:
        organisations = paginator.page(1)
    except EmptyPage:
        organisations = paginator.page(paginator.num_pages) 

    return render(request, 'all_organisations.html', {'organisations': organisations})


def projects(request):

    myprojects = Projects.objects.all().values()

    # use paginator to display 100 projects at the time 
    paginator = Paginator(myprojects, 100)
    page = request.GET.get('page')
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        projects = paginator.page(1)
    except EmptyPage:
        projects = paginator.page(paginator.num_pages) 

    return render(request, 'all_projects.html', {'projects': projects})
