from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

def trys(request):
  template = loader.get_template('students/try.html')
  return HttpResponse(template.render())

