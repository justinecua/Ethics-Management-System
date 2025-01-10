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
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password1,
            )

            student = Student.objects.create(
                auth_user=user,
            )

            student_account_type = Account_Type.objects.get(Account_type='Admin')

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

