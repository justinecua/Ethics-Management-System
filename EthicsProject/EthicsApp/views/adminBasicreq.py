from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import BasicRequirements
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

@csrf_exempt
def adminBasicreq(request):
    if request.method == 'POST':
          basicRequirements = request.POST.get('basicRequirements')

    if not basicRequirements:
            messages.error(request, "Basic Requirements required.")
            return redirect('adminManuscripts')  

    try:
            BasicRequirements.objects.create(
                basicRequirements=basicRequirements,
            )
            messages.success(request, "Basic Requirements added successfully!")
    except Exception as e:
            messages.error(request, f"An error occurred: {e}")

    return redirect('adminManuscripts')



