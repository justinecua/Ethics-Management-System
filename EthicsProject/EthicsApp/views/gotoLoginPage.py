from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

def login2(request):
  template = loader.get_template('accounts/login.html')
  return HttpResponse(template.render())

def homeLogin(request):
  template = loader.get_template('accounts/login.html')
  return HttpResponse(template.render())
