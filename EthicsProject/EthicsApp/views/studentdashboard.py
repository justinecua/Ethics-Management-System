from django.template import loader
from django.http import HttpResponse


def studentdashboard(request):
  template = loader.get_template('students/studentdashboard.html')
  return HttpResponse(template.render())