from django.urls import path
from . import views

urlpatterns = [
    path('', views.podcast_list, name='podcast_list'),
    path('add-new-podcast/', views.add_new_podcast, name='add_new_podcast'),
    path('view-podcast/<int:podcast_id>/', views.view_podcast, name='view_podcast'),
]