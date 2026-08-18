from django.contrib import admin
from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):

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
        "description",
    )

    ordering = (
        "-published_at",
    )

    readonly_fields = (
        "published_at",
    )
    