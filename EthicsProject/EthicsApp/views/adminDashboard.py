from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Student, Reviewer

def adminDashboard(request):
    return render(request, 'admin/adminDashboard.html')

def adminAccounts(request):
    students = Student.objects.filter(auth_user__isnull=False, auth_user__is_superuser=False).prefetch_related('accounts_set')
    reviewers = Reviewer.objects.all()
    admins = Student.objects.filter(auth_user__isnull=False, auth_user__is_superuser=True).prefetch_related('accounts_set')
    
    return render(request, 'admin/adminAccounts.html', {
        'students': students,
        'reviewers': reviewers,
        'admins': admins
    })

def adminAppointments(request):
    return render(request, 'admin/adminAppointments.html')

def adminManuscripts(request):
    return render(request, 'admin/adminManuscripts.html')

def adminSchedule(request):
    return render(request, 'admin/adminSchedule.html')

def adminSettings(request):
    return render(request, 'admin/adminSettings.html')

def adminHelpSupport(request):
    return render(request, 'admin/adminHelp&Support.html')

