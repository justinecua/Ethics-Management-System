from django.shortcuts import render
from django.db.models import Prefetch
from .models import Student, Accounts, Reviewer, Account_Type

def get_google_profile_picture(user):
    social_account = user.socialaccount_set.filter(provider='google').first()
    if social_account:
        return social_account.extra_data.get('picture')
    return None

def adminDashboard(request):
    # Retrieve profile picture and account type from session
    profile_picture = request.session.get('profile_picture', None)
    account_type = request.session.get('account_type', None)

    context = {
        'profile_picture': profile_picture,
        'account_type': account_type,
    }
    return render(request, 'admin/adminDashboard.html', context)

def adminAccounts(request):
    # Retrieve profile picture and account type from session
    profile_picture = request.session.get('profile_picture', None)
    account_type = request.session.get('account_type', None)

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
    
    for student in students:
        student.google_picture = get_google_profile_picture(student.auth_user)
    
    for reviewer in reviewers:
        reviewer.google_picture = get_google_profile_picture(reviewer.auth_user)
    
    for admin in admins:
        admin.google_picture = get_google_profile_picture(admin.auth_user)

    return render(request, 'admin/adminAccounts.html', {
        'students': students,
        'reviewers': reviewers,
        'admins': admins,
        'accountTypes': accountType,
        'profile_picture': profile_picture,
        'account_type': account_type,
    })

def adminAppointments(request):
    # Retrieve profile picture and account type from session
    profile_picture = request.session.get('profile_picture', None)
    account_type = request.session.get('account_type', None)

    return render(request, 'admin/adminAppointments.html', {
        'profile_picture': profile_picture,
        'account_type': account_type
    })

# Similarly modify other admin views...
def adminManuscripts(request):
    profile_picture = request.session.get('profile_picture', None)
    account_type = request.session.get('account_type', None)
    
    return render(request, 'admin/adminManuscripts.html', {
        'profile_picture': profile_picture,
        'account_type': account_type
    })

def adminSchedule(request):
    profile_picture = request.session.get('profile_picture', None)
    account_type = request.session.get('account_type', None)
    
    return render(request, 'admin/adminSchedule.html', {
        'profile_picture': profile_picture,
        'account_type': account_type
    })

def adminSettings(request):
    profile_picture = request.session.get('profile_picture', None)
    account_type = request.session.get('account_type', None)
    
    return render(request, 'admin/adminSettings.html', {
        'profile_picture': profile_picture,
        'account_type': account_type
    })

def adminHelpSupport(request):
    profile_picture = request.session.get('profile_picture', None)
    account_type = request.session.get('account_type', None)
    
    return render(request, 'admin/adminHelp&Support.html', {
        'profile_picture': profile_picture,
        'account_type': account_type
    })


