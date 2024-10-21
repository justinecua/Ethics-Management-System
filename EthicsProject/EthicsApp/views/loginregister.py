from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Account_Type, Accounts, Student
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password1 == password2:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
            )

            student = Student.objects.create(
                auth_user=user,
            )

            student_account_type = Account_Type.objects.get(Account_type='Student')

            newAcc = Accounts.objects.create(
                student_id=student,
                account_typeid=student_account_type
            )

            user = authenticate(request, username=username, password=password1)
            if user is not None:
                login(request, user)  
                return redirect('studentdashboard')
        else:    
            messages.error(request, "Passwords do not match.")

    return render(request, 'gotoRegisterPage.html')

from allauth.socialaccount.models import SocialAccount

@csrf_exempt
def validatelogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            try:
                profile = Accounts.objects.get(student_id__auth_user=user)
                account_type = profile.account_typeid.Account_type
                
                social_account = SocialAccount.objects.filter(user=user, provider='google').first()
                profile_picture = social_account.extra_data.get('picture') if social_account else None
                
                request.session['profile_picture'] = profile_picture
                request.session['account_type'] = account_type

                if account_type == 'Student':
                    return redirect('studentdashboard')
                elif account_type == 'Admin':
                    return redirect('adminDashboard')
                elif account_type == 'Reviewer':
                    return redirect('schedule_dashboard')
                else:
                    return redirect('defaultdashboard')

            except Accounts.DoesNotExist:
                messages.error(request, "User profile not found.")
                return redirect('login')

        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'gotoLoginPage.html')




