from django.http import HttpResponse
from django.template import loader

def EC_funding(request):
  template = loader.get_template('start.html')
  return HttpResponse(template.render())