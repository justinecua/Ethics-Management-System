from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import College, EthicalRiskQuestions
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

@csrf_exempt
def adminAddEthicalRiskQuestions(request):
    if request.method == 'POST':
        ethicalQuestions = request.POST.get('ethical-questions')

        # Only show an error if ethicalQuestions is empty
        if not ethicalQuestions:
            messages.error(request, "Ethical question is required.")
            return redirect('adminEthicalRiskQuestions')  

        try:
            EthicalRiskQuestions.objects.create(
                ethicalQuestions=ethicalQuestions
            )
            messages.success(request, "Ethical Question added successfully!")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")

        return redirect('adminEthicalRiskQuestions')

    return redirect('adminEthicalRiskQuestions')


