from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from urllib.parse import urlparse
from django.db.models import Q
from urllib.parse import urlparse, parse_qs

from .models import Podcast



def get_youtube_video_id(url):

    if not url:
        return None

    try:
        parsed_url = urlparse(url)

        hostname = (parsed_url.hostname or "").lower()

        # youtu.be/VIDEO_ID
        if hostname in ["youtu.be", "www.youtu.be"]:
            return parsed_url.path.strip("/").split("/")[0]

        # youtube.com
        if hostname in [
            "youtube.com",
            "www.youtube.com",
            "m.youtube.com",
        ]:

            # youtube.com/watch?v=VIDEO_ID
            if parsed_url.path == "/watch":
                query = parse_qs(parsed_url.query)
                return query.get("v", [None])[0]

            # youtube.com/embed/VIDEO_ID
            # youtube.com/shorts/VIDEO_ID
            # youtube.com/live/VIDEO_ID
            parts = parsed_url.path.strip("/").split("/")

            if len(parts) >= 2 and parts[0] in [
                "embed",
                "shorts",
                "live",
            ]:
                return parts[1]

    except (ValueError, IndexError):
        return None

    return None


def podcast_list(request):

    query = request.GET.get(
        "q",
        ""
    ).strip()

    podcasts_queryset = Podcast.objects.filter(
        is_active=True
    )

    # البحث بالعنوان
    if query:
        podcasts_queryset = podcasts_queryset.filter(
            Q(title__icontains=query)
        )

    podcasts_queryset = podcasts_queryset.order_by(
        "-published_at"
    )

    podcasts = list(
        podcasts_queryset
    )

    # تجهيز صورة YouTube لكل بودكاست
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


    # أول 3 بودكاست
    featured_podcasts = podcasts[:3]

    # بقية البودكاست
    more_podcasts = podcasts[3:]


    context = {
        "featured_podcasts": featured_podcasts,
        "more_podcasts": more_podcasts,
        "query": query,
    }


    return render(
        request,
        "podcast/podcast.html",
        context
    )






def add_new_podcast(request):

    if request.method == "POST":

        title = request.POST.get(
            "title",
            ""
        ).strip()

        youtube_url = request.POST.get(
            "youtube_url",
            ""
        ).strip()

        image = request.FILES.get(
            "image"
        )


        # التحقق من العنوان
        if not title:

            return render(
                request,
                "podcast/add_new_podcast.html",
                {
                    "error": "يرجى إدخال عنوان البودكاست.",
                    "title": title,
                    "youtube_url": youtube_url,
                }
            )


        # التحقق من الرابط
        if not youtube_url:

            return render(
                request,
                "podcast/add_new_podcast.html",
                {
                    "error": "يرجى إدخال رابط البودكاست على يوتيوب.",
                    "title": title,
                    "youtube_url": youtube_url,
                }
            )


        # التأكد أن الرابط من YouTube
        try:

            parsed_url = urlparse(youtube_url)

            hostname = (
                parsed_url.hostname or ""
            ).lower()

            allowed_hosts = (
                "youtube.com",
                "www.youtube.com",
                "m.youtube.com",
                "youtu.be",
            )

            if hostname not in allowed_hosts:

                return render(
                    request,
                    "podcast/add_new_podcast.html",
                    {
                        "error": "يرجى إدخال رابط صحيح من YouTube.",
                        "title": title,
                        "youtube_url": youtube_url,
                    }
                )

        except ValueError:

            return render(
                request,
                "podcast/add_new_podcast.html",
                {
                    "error": "رابط يوتيوب غير صالح.",
                    "title": title,
                    "youtube_url": youtube_url,
                }
            )


        # إنشاء البودكاست
        Podcast.objects.create(
            title=title,
            youtube_url=youtube_url,
            image=image,
            is_active=True
        )


        messages.success(
            request,
            "تم نشر البودكاست بنجاح"
        )


        return redirect(
            "add_new_podcast"
        )


    return render(
        request,
        "podcast/add_new_podcast.html"
    )



def view_podcast(request, podcast_id):

    podcast = get_object_or_404(
        Podcast,
        id=podcast_id,
        is_active=True
    )


    # استخراج معرف فيديو YouTube
    video_id = get_youtube_video_id(
        podcast.youtube_url
    )


    if video_id:

        youtube_embed_url = (
            f"https://www.youtube.com/embed/"
            f"{video_id}"
        )

        youtube_thumbnail = (
            f"https://img.youtube.com/vi/"
            f"{video_id}/hqdefault.jpg"
        )

    else:

        youtube_embed_url = None
        youtube_thumbnail = None


    # بودكاستات ذات صلة
    related_podcasts = list(

        Podcast.objects
        .filter(is_active=True)
        .exclude(id=podcast.id)
        .order_by("-published_at")[:5]

    )


    # تجهيز صور البودكاستات ذات الصلة
    for related in related_podcasts:

        related_video_id = (
            get_youtube_video_id(
                related.youtube_url
            )
        )


        if related_video_id:

            related.youtube_thumbnail = (
                f"https://img.youtube.com/vi/"
                f"{related_video_id}/"
                f"hqdefault.jpg"
            )

        else:

            related.youtube_thumbnail = None


    context = {

        "podcast": podcast,

        "youtube_embed_url":
            youtube_embed_url,

        "youtube_thumbnail":
            youtube_thumbnail,

        "related_podcasts":
            related_podcasts,
    }


    return render(
        request,
        "podcast/view_podcast.html",
        context
    )

