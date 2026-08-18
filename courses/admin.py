from django.contrib import admin
from .models import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):

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
        "link",
    )

    ordering = (
        "-published_at",
    )

    readonly_fields = (
        "published_at",
    )