from django.shortcuts import render


def studentAppointment(request):
    return render(request, 'students/studentappointment.html')


def studentManuscript(request):
    return render(request, 'students/studentmanuscript.html')

def studentSettings(request):
    return render(request, 'students/studentSettings.html')