from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

def signup(request):
  template = loader.get_template('accounts/signup.html')
  return HttpResponse(template.render())

