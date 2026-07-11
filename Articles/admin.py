from django.contrib import admin
from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        "author_name",

        "status",
    )
    list_filter = (
        "field",
        "category",
        "created_at",
        "status",
    )
    search_fields = (
        "author_name",
        "content",
    )
    ordering = ("-created_at",)

    list_editable = ['status']