from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Category
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

@csrf_exempt
def adminAddCategory(request):
    if request.method == 'POST':
        category_name = request.POST.get('category-name')

        if not category_name:
            messages.error(request, "Category name required.")
            return redirect('adminManuscripts')  

        try:
            Category.objects.create(
                category_name=category_name,
            )
            messages.success(request, "Category added successfully!")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")

        return redirect('adminManuscripts')

    return redirect('adminManuscripts')


