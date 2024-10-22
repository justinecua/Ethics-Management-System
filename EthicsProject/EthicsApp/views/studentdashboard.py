from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render

def studentdashboard(request):
    profile_picture = request.session.get('profile_picture', None)
    account_type = request.session.get('account_type', None)
    
    context = {
        'profile_picture': profile_picture,
        'account_type': account_type,
    }
    return render (request, 'students/studentdashboard.html', context) 
