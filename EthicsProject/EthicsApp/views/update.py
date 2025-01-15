from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render, redirect
from .models import Category

@csrf_exempt
def update_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == 'POST':
        category_name = request.POST.get('category_name')

        if not category_name:
            return JsonResponse({'success': False, 'message': 'Category name is required'}, status=400)

        category.category_name = category_name
        category.save()

        return redirect('adminManuscripts')


    return render(request, 'admin/updateCategory.html', {'category': category})
