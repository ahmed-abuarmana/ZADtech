from django.shortcuts import get_object_or_404, render
from .models import Category, Courses, Field


from django.shortcuts import render, redirect
from .models import Category, Field, Courses

def add_new_course(request):
    categories = Category.objects.all()
    fields = Field.objects.all()

    if request.method == "POST":
        category = Category.objects.get(id=request.POST["category"]) if request.POST["category"] else None
        field = Field.objects.get(id=request.POST["field"]) if request.POST["field"] else None

        Courses.objects.create(
            title=request.POST["title"],
            teacher_name=request.POST["teacher_name"],
            channel_name=request.POST["channel_name"],
            category=category,
            field=field,
            language=request.POST["language"],
            duration=request.POST["duration"],
            description=request.POST["description"],
            link=request.POST["link"],
            thumbnail=request.FILES.get("thumbnail"),
            level=request.POST["level"],
            is_free="is_free" in request.POST,
            certificate="certificate" in request.POST,
        )

        return redirect("add_new_course")  
    

    context = {
        "categories": categories,
        "fields": fields,
        "SuccessMessage": "تم إضافة الكورس بنجاح!" if request.method == "POST" else "",
        "ErrorMessage": "حدث خطأ أثناء إضافة الكورس." if request.method == "POST" and not request.POST else "",
    }
    return render(request, "courses/add_new_course.html", context)



def courses(request):
    categories = Category.objects.filter(is_active=True)[:3]
    courses = Courses.objects.filter(status=True)[:3]
    context = {
        'categories': categories,
        'courses': courses,
    }
    return render(request, "courses/courses.html", context)


def view_course(request, course_id, course_name):
    course = get_object_or_404(Courses, id=course_id)
    context = {
        'course': course,
    }
    return render(request, "courses/view_course.html", context)


def all_courses(request):

    courses = Courses.objects.filter(status=True)

    categories = Category.objects.filter(is_active=True)
    fields = Field.objects.filter(is_active=True)

    # ===== Filters =====
    category_id = request.GET.get("category")
    field_id = request.GET.get("field")
    level = request.GET.get("level")
    is_free = request.GET.get("is_free")

    if category_id:
        courses = courses.filter(category_id=category_id)

    if field_id:
        courses = courses.filter(field_id=field_id)

    if level:
        courses = courses.filter(level=level)

    if is_free in ["true", "false"]:
        courses = courses.filter(is_free=(is_free == "true"))

    context = {
        "courses": courses,
        "categories": categories,
        "fields": fields,
    }

    return render(request, "courses/all_courses.html", context)
