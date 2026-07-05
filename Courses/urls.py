from django.urls import path 
from . import views

urlpatterns = [
    path("", views.courses, name="courses"),
    path("add-new-course/", views.add_new_course, name="add_new_course"),
    path("view-course/<int:course_id>/<str:course_name>/", views.view_course, name="view_course"),
    path("all-courses/", views.all_courses, name="all_courses"),
]
