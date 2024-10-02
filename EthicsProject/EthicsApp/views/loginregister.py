from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages


@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password')
        password2 = request.POST.get('password2')

        # Create the user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
        )

        # Authenticate and log in the user
        user = authenticate(request, username=username, password=password1)
        if user is not None:
            auth_login(request, user)
            return redirect('studentdashboard')  # Make sure 'dashboard' is a valid URL name in your app

    return render(request, 'master.html')





@csrf_exempt
def validatelogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Log in the user
            auth_login(request, user)
            return redirect('studentdashboard')  # Redirect to the student dashboard after successful login
        else:
            # Invalid credentials
            messages.error(request, "Invalid username or password.")
    
    # Render the login page
    return render(request, 'master.html')  # Make sure your login template is named 'login.html'



