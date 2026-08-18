from django.shortcuts import render
from .models import Quotes
import random
from django.db.models import Q
from urllib.parse import urlparse, parse_qs
from books.models import Book
from courses.models import Course
from articles.models import Article
from podcast.models import Podcast


def index(request):
    quotes = list(Quotes.objects.all())

    random_quote = random.choice(quotes) if quotes else None

    context = {
        "random_quote": random_quote,
    }

    return render(request, "core/index.html", context)


def about(request):

    query = request.GET.get(
        "q",
        ""
    ).strip()


    # ========================================
    # الكتب
    # ========================================

    books = Book.objects.filter(
        is_active=True
    )


    # ========================================
    # الدورات
    # ========================================

    courses = Course.objects.filter(
        is_active=True
    )


    # ========================================
    # المقالات
    # ========================================

    articles = Article.objects.filter(
        is_active=True
    )


    # ========================================
    # البودكاست
    # ========================================

    podcasts = Podcast.objects.filter(
        is_active=True
    )


    # ========================================
    # البحث
    # ========================================

    if query:

        books = books.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )


        courses = courses.filter(
            Q(title__icontains=query)
        )


        articles = articles.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )


        podcasts = podcasts.filter(
            Q(title__icontains=query)
        )


    # ========================================
    # آخر 9 عناصر من كل قسم
    # ========================================

    books = list(
        books.order_by("-id")[:9]
    )

    courses = list(
        courses.order_by("-id")[:9]
    )

    articles = list(
        articles.order_by("-id")[:9]
    )

    podcasts = list(
        podcasts.order_by("-id")[:9]
    )


    # ========================================
    # تجهيز صور YouTube للبودكاست
    # ========================================

    for podcast in podcasts:

        video_id = get_youtube_video_id(
            podcast.youtube_url
        )


        if video_id:

            podcast.youtube_thumbnail = (
                f"https://img.youtube.com/vi/"
                f"{video_id}/hqdefault.jpg"
            )

        else:

            podcast.youtube_thumbnail = None


    context = {

        "books": books,

        "courses": courses,

        "articles": articles,

        "podcasts": podcasts,

        "query": query,

        "books_count": len(books),

        "courses_count": len(courses),

        "articles_count": len(articles),

        "podcasts_count": len(podcasts),

    }


    return render(
        request,
        "core/about.html",
        context
    )

def login(request):
    return render(request, "authentication/login.html")


def profile(request):
    return render(request, "core/profile.html")



def get_youtube_video_id(url):

    if not url:
        return None

    try:

        parsed_url = urlparse(url)

        hostname = (
            parsed_url.hostname or ""
        ).lower()


        # youtu.be/VIDEO_ID
        if hostname in [
            "youtu.be",
            "www.youtu.be",
        ]:

            return (
                parsed_url.path
                .strip("/")
                .split("/")[0]
            )


        # youtube.com
        if hostname in [
            "youtube.com",
            "www.youtube.com",
            "m.youtube.com",
        ]:


            # youtube.com/watch?v=VIDEO_ID
            if parsed_url.path == "/watch":

                query = parse_qs(
                    parsed_url.query
                )

                return query.get(
                    "v",
                    [None]
                )[0]


            # shorts / embed / live
            parts = (
                parsed_url.path
                .strip("/")
                .split("/")
            )


            if (
                len(parts) >= 2
                and parts[0] in [
                    "embed",
                    "shorts",
                    "live",
                ]
            ):

                return parts[1]


    except (
        ValueError,
        IndexError,
    ):

        return None


    return None
