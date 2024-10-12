from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Student, Accounts, Reviewer, Account_Type
from django.db.models import Prefetch

def adminDashboard(request):
    return render(request, 'admin/adminDashboard.html')

def adminAccounts(request):
    students = Student.objects.filter(
        auth_user__isnull=False,
        auth_user__is_superuser=False
    ).prefetch_related(
        Prefetch(
            'accounts_set',
            queryset=Accounts.objects.filter(account_typeid__Account_type='Student')
        )
    )

    reviewers = Reviewer.objects.filter(
        auth_user__isnull=False,
        auth_user__is_superuser=False
    ).prefetch_related(
        Prefetch(
            'accounts_set',
            queryset=Accounts.objects.filter(account_typeid__Account_type='Reviewer')
        )
    )

    admins = Student.objects.filter(
        auth_user__isnull=False,
        auth_user__is_superuser=True
    ).prefetch_related(
        Prefetch(
            'accounts_set',
            queryset=Accounts.objects.filter(account_typeid__Account_type='Admin')
        )
    )    
    accountType = Account_Type.objects.exclude(Account_type='Student')

    return render(request, 'admin/adminAccounts.html', {
        'students': students,
        'reviewers': reviewers,
        'admins': admins,
        'accountTypes': accountType,
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

