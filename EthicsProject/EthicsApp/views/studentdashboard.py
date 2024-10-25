from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def studentdashboard(request):
  template = loader.get_template('students/studentdashboard.html')
  return HttpResponse(template.render())

