from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render
from .models import Accounts 
from django.contrib.auth.models import User


def reviewerdashboard(request):
    profile_picture = request.session.get('profile_picture', None)
    account_type = request.session.get('account_type', None)
    username = request.session.get('username', None)
    is_new_user = check_user(request)
    
    context = {
        'profile_picture': profile_picture,
        'account_type': account_type,
        'username': username,
        'is_new_user': is_new_user,
    }
    return render (request, 'Reviewer/reviewerDashboard.html', context)

def reviewerManuscript(request):
    profile_picture = request.session.get('profile_picture', None)
    account_type = request.session.get('account_type', None)
    
    context = {
        'profile_picture': profile_picture,
        'account_type': account_type,
    }
    return render(request, 'Reviewer/reviewerManuscripts.html', context)

def reviewerSettings(request):
    profile_picture = request.session.get('profile_picture', None)
    account_type = request.session.get('account_type', None)
    
    context = {
        'profile_picture': profile_picture,
        'account_type': account_type,
    }
    return render(request, 'Reviewer/reviewerSettings.html', context)

def reviewerSchedule(request):
    profile_picture = request.session.get('profile_picture', None)
    account_type = request.session.get('account_type', None)
    
    context = {
        'profile_picture': profile_picture,
        'account_type': account_type,
    }
    return render(request, 'Reviewer/reviewerSchedule.html', context)

def check_user(request):
    if request.user.is_authenticated:
        user_exists = User.objects.filter(id=request.user.id).exists()
        account_exists = Accounts.objects.filter(student_id=request.user.id).exists()
        is_new_user = not (user_exists and account_exists)

        return is_new_user
    else:
        return False
