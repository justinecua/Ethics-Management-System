from django.shortcuts import render


def studentAppointment(request):
    return render(request, 'students/studentappointment.html')