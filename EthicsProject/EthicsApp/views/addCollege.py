from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import College
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

@csrf_exempt
def adminAddColleges(request):
    if request.method == 'POST':
        collegeInitial = request.POST.get('college-initial')
        collegeName = request.POST.get('college-name')

        if not collegeInitial or not collegeName:
            messages.error(request, "Both college initial and name are required.")
            return redirect('adminColleges')  

        try:
            College.objects.create(
                college_name=collegeName,
                college_initials=collegeInitial
            )
            messages.success(request, "College added successfully!")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")

        return redirect('adminColleges')

    return redirect('adminColleges')


