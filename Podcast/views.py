from django.shortcuts import render

# Create your views here.

def podcasts(request):
    return render(request, "podcast/podcast.html")
