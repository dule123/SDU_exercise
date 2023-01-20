from django.http import HttpResponse
from django.template import loader
from .models import Organisations
from .models import Projects
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage
from django.shortcuts import render
from django.db.models import Sum, F

# next two lines prevent matplot lib from trying to graphically display the plot and avoid some error msgs
import matplotlib as mpl
mpl.use('Agg')

import matplotlib.pyplot as plt
from django.db.models.functions import Coalesce
from decimal import Decimal
from django.db.models import F, Case, When

def main(request):
  template = loader.get_template('main.html')
  return HttpResponse(template.render())

def organisations(request):

    # select onlt the unique organisations, based on the organisationID
    myorganisations = Organisations.objects.all().values().order_by('name').distinct('name')

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

    myprojects = Projects.objects.all().values().order_by('acronym')

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

def detail_project(request, id):
  myproject = Projects.objects.get(id=id)
  template = loader.get_template('detail_project.html')
  context = {
    'myproject': myproject,
  }
  return HttpResponse(template.render(context, request))

def detail_organisation(request, id):
  myorganisation = Organisations.objects.get(id=id)
  template = loader.get_template('detail_organisation.html')
  context = {
    'myorganisation': myorganisation,
  }
  return HttpResponse(template.render(context, request))

def total_funds_per_country(request):
    # Query the database to get the total amount of funds per country
    # as there are too many countries, sort it and take only top 10 to plot 
    num_cuntries_to_plot = 10
    funds_per_country = Organisations.objects.exclude(ecContribution=Decimal('NaN')).values('country').annotate(total_funds=Sum('ecContribution')).order_by('-total_funds')[:num_cuntries_to_plot]
    
    # Extract the country names and total funds from the queryset
    countries = [item['country'] for item in funds_per_country]
    funds = [item['total_funds'] for item in funds_per_country]

    # Some quick prints to check what's going on...  
    # print (top_10_funds_per_country)
    # print (countries)
    # print (funds)
    # unique_countries = Organisations.objects.exclude(ecContribution=Decimal('NaN')).values_list('country', flat=True).distinct()
    # print(unique_countries)
    # number_of_countries = Organisations.objects.exclude(ecContribution=Decimal('NaN')).values_list('country', flat=True).distinct().count()
    # print(number_of_countries)

    # Create the bar chart
    plt.bar(countries, funds)

    # Add labels to the x and y axes
    plt.xlabel('Country')
    plt.ylabel('Total Funds (in €)')

    # Save the plot to a file
    plt.savefig('media/total_funds_per_country.png')

    # plt.bar(countries, funds).savefig('total_funds_per_country.png')

    # Render the template and pass the file name to it
    return render(request, 'plot_funding.html', {'plot': 'total_funds_per_country.png'})