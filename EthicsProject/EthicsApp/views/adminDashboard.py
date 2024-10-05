from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

def adminDashboard(request):
  template = loader.get_template('admin/admin_dashboard.html')
  return HttpResponse(template.render())

