from django.shortcuts import render
from .models import Category




def courses(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, "courses/courses.html", context)
