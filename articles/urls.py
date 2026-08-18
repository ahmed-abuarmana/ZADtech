from django.urls import path
from . import views

urlpatterns = [
    path('', views.article_list, name='article_list'),
    path('add-new-article/', views.add_new_article, name='add_new_article'),
    path('view-article/<int:article_id>/', views.view_article, name='view_article'),
]