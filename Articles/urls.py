from django.urls import path 
from . import views

urlpatterns = [
    path("", views.articles, name="articles"),
    path("add_new_article/", views.add_new_article, name="add_new_article"),
    path("show_all_articles/", views.show_all_articles, name="show_all_articles"),
    

]
