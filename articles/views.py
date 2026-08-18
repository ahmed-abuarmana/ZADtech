from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Article




def article_list(request):

    articles = Article.objects.filter(
        is_active=True
    ).order_by("-published_at")


    Recently_published_articles = articles[:3]


    Related_articles = articles[3:6]


    total_articles = articles.count()


    context = {
        "Recently_published_articles": Recently_published_articles,
        "Related_articles": Related_articles,
        "total_articles": total_articles,
    }


    return render(
        request,
        "articles/articles.html",
        context
    )



def add_new_article(request):

    if request.method == "POST":

        title = request.POST.get(
            "title",
            ""
        ).strip()

        description = request.POST.get(
            "description",
            ""
        ).strip()

        image = request.FILES.get(
            "image"
        )


        # التحقق من العنوان
        if not title:

            return render(
                request,
                "articles/add_new_article.html",
                {
                    "error": "يرجى إدخال عنوان المقال.",
                    "title": title,
                    "description": description,
                }
            )


        # التحقق من المحتوى
        if not description:

            return render(
                request,
                "articles/add_new_article.html",
                {
                    "error": "يرجى إدخال محتوى المقال.",
                    "title": title,
                    "description": description,
                }
            )


        # إنشاء المقال
        Article.objects.create(
            title=title,
            description=description,
            image=image,
            is_active=True
        )


        messages.success(
            request,
            "تم نشر المقال بنجاح"
        )


        return redirect(
            "add_new_article"
        )


    return render(
        request,
        "articles/add_new_article.html"
    )


def view_article(request, article_id):

    article = get_object_or_404(
        Article,
        id=article_id,
        is_active=True
    )

    related_articles = (
        Article.objects
        .filter(is_active=True)
        .exclude(id=article.id)
        .order_by("-published_at")[:5]
    )

    context = {
        "article": article,
        "related_articles": related_articles,
    }

    return render(
        request,
        "articles/view_article.html",
        context
    )

