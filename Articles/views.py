from django.shortcuts import render, redirect
from requests import get, request
from Courses.models import Field, Category
from .models import Article

from django.contrib import messages


# Create your views here.

def articles(request):
    Recently_published_articles = Article.objects.filter(status=True).order_by("-created_at")[:3]
    Related_articles = Article.objects.filter(status=True).order_by("-created_at")[:2]
    context = {
        "Recently_published_articles": Recently_published_articles,
        "Related_articles": Related_articles
    }

    return render(request, "articles/articles.html", context)


def add_new_article(request):
    if request.method == "POST":

        category = Category.objects.get(id=request.POST.get("category"))
        field = Field.objects.get(id=request.POST.get("field"))

        Article.objects.create(
            author_name=request.POST.get("author_name"),
            category=category,
            field=field,
            content=request.POST.get("content"),
            image=request.FILES.get("image"),
        )
        
        messages.success(request, "تم إرسال مقالك بنجاح، وسيتم مراجعته قبل النشر.")
        return redirect("add_new_article")

    context = {
        "fields": Field.objects.all(),
        "categories": Category.objects.all(),
    }

    return render(request, "articles/add_new_article.html", context)



def show_all_articles(request):
    articles = Article.objects.filter(status=True).order_by("-created_at")
    context = {
        "articles": articles
    }
    return render(request, "articles/show_all_articles.html", context)