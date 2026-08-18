from django.urls import path
from . import views

urlpatterns = [
    path('', views.courses_list, name='courses_list'),
    path('add-new-course/', views.add_new_course, name="add_new_course"),
    path('view-course/<int:course_id>/', views.view_course, name="view_course"),
    path('all-courses/', views.all_courses, name='all_courses'),
]
