from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('view-book/<int:book_id>/', views.view_book, name='view_book'),
    path('add-new-book/', views.add_new_book, name='add_new_book'),
]