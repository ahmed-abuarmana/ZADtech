from django.shortcuts import render
from requests import request

# Create your views here.

def articles(request):
    return render(request, "articles/articles.html")
