from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

def login2(request):
  template = loader.get_template('accounts/login.html')
  return HttpResponse(template.render())

def homeLogin(request):
  template = loader.get_template('accounts/login.html')
  return HttpResponse(template.render())

from django.contrib.auth import logout
from django.shortcuts import render, redirect
  
def accounts_logout(request):
    if request.method == 'POST':
        logout(request)  # Logs the user out
        return redirect('login2')  # Redirect to login or homepage after logout
    return render(request, 'accounts/logout.html') 

def reviewer_logout(request):
    if request.method == 'POST':
        logout(request)  # Logs the user out
        return redirect('login2')  # Redirect to login or homepage after logout
    return render(request, 'accounts/reviewerLogout.html') 

def admin_logout(request):
    if request.method == 'POST':
        logout(request)  # Logs the user out
        return redirect('login2')  # Redirect to login or homepage after logout
    return render(request, 'accounts/adminLogout.html') 