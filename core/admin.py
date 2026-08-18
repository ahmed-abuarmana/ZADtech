from django.contrib import admin
from .models import Quotes


@admin.register(Quotes)
class QuotesAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'author')
    search_fields = ('text', 'author')
    