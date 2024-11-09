from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import SupplementaryRequirements
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

@csrf_exempt
def adminSDreq(request):
    if request.method == 'POST':
          supplementaryRequirements = request.POST.get('supplementaryRequirements')

    if not supplementaryRequirements:
            messages.error(request, "Basic Requirements required.")
            return redirect('adminManuscripts')  

    try:
            SupplementaryRequirements.objects.create(
                supplementaryRequirements=supplementaryRequirements,
            )
            messages.success(request, "Supplementary added successfully!")
    except Exception as e:
            messages.error(request, f"An error occurred: {e}")

    return redirect('adminManuscripts')



