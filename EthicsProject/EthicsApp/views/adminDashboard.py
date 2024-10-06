from django.shortcuts import render

def adminDashboard(request):
    return render(request, 'admin/adminDashboard.html')

def adminAccounts(request):
    return render(request, 'admin/adminAccounts.html')

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

