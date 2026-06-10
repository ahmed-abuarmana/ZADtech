from django.shortcuts import render
from .models import Quotes
import random

def index(request):
    quotes = Quotes.objects.all()
    random_quote = random.choice(quotes) if quotes else None
    context = {
        'random_quote': random_quote,
    }
    return render(request, "core/index.html", context)

