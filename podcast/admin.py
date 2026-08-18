from django.contrib import admin
from .models import Podcast


@admin.register(Podcast)
class PodcastAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "is_active",
        "published_at",
    )

    list_filter = (
        "is_active",
        "published_at",
    )

    search_fields = (
        "title",
        "youtube_url",
    )

    ordering = (
        "-published_at",
    )

    readonly_fields = (
        "published_at",
    )
    