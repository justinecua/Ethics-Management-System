from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Account_Type, Accounts, Student
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from allauth.socialaccount.models import SocialAccount
from django.db.models import Q

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
                account_typeid=student_account_type
            )

            user = authenticate(request, username=username, password=password1)
            if user is not None:
                login(request, user)

                social_account = SocialAccount.objects.filter(user=user, provider='google').first()
                profile_picture = social_account.extra_data.get('picture') if social_account else None

                request.session['profile_picture'] = profile_picture
                request.session['account_type'] = student_account_type.Account_type
                request.session['username'] = user.username

                return redirect('studentdashboard')
        else:
            messages.error(request, "Passwords do not match.")

    return render(request, 'accounts/login.html')

@csrf_exempt
def validatelogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user is not None:
            user = authenticate(request, username=user.username, password=password)

        if user is not None:
            login(request, user)

            try:
                profile = Accounts.objects.filter(
                    Q(student_id__auth_user=user) |
                    Q(reviewer_id__auth_user=user) |
                    Q(account_typeid__Account_type='Student', student_id__isnull=True)
                ).first()

                if profile:
                    account_type = profile.account_typeid.Account_type

                    social_account = SocialAccount.objects.filter(user=user, provider='google').first()
                    profile_picture = social_account.extra_data.get('picture') if social_account else None

                    request.session['profile_picture'] = profile_picture
                    request.session['account_type'] = account_type
                    request.session['username'] = user.username

                    if account_type == 'Student':
                        return redirect('studentdashboard')
                    elif account_type == 'Admin':
                        return redirect('adminDashboard')
                    elif account_type == 'Reviewer':
                        return redirect('reviewerdashboard')
                    else:
                        return redirect('defaultdashboard')

                else:
                    messages.error(request, "User profile not found.")
                    return redirect('validatelogin')

            except Accounts.DoesNotExist:
                messages.error(request, "User profile not found.")
                return redirect('validatelogin')

        else:
            messages.error(request, "Invalid email or password.")

    return render(request, 'accounts/login.html')





