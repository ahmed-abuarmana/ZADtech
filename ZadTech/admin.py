from django.contrib import admin
from .models import Quotes

@admin.register(Quotes)
class QuotesAdmin(admin.ModelAdmin):
    list_display = ('author', 'text')
    search_fields = ('author', 'text')

