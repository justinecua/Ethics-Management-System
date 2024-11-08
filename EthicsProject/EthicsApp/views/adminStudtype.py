from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import TypeOfStudy
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

@csrf_exempt
def adminStudtype(request):
    if request.method == 'POST':
         type_of_study = request.POST.get('type_of_study')

    if not type_of_study:
            messages.error(request, "Type of Study required.")
            return redirect('adminManuscripts')  

    try:
            TypeOfStudy.objects.create(
                 type_of_study= type_of_study,
            )
            messages.success(request, "Type of Study added successfully!")
    except Exception as e:
            messages.error(request, f"An error occurred: {e}")

    return redirect('adminManuscripts')



