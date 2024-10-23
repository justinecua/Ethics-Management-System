from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render


def studentdashboard(request):
  template = loader.get_template('students/studentdashboard.html')
  return HttpResponse(template.render())

def student_appointment(request):
    return render(request, 'students/studentAppointment.html')