from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Course



def courses_list(request):

    # كلمة البحث
    query = request.GET.get("q", "").strip()

    # الدورات الفعالة فقط
    courses_queryset = Course.objects.filter(
        is_active=True
    )

    # البحث في عنوان الدورة
    if query:
        courses_queryset = courses_queryset.filter(
            Q(title__icontains=query)
        )

    # الأحدث أولاً
    courses_queryset = courses_queryset.order_by(
        "-published_at"
    )

    # Pagination
    paginator = Paginator(
        courses_queryset,
        6
    )

    page_number = request.GET.get("page")

    courses = paginator.get_page(
        page_number
    )

    # أول 3 دورات للقسم العلوي
    featured_courses = Course.objects.filter(
        is_active=True
    ).order_by("-published_at")[:3]

    context = {
        "courses": courses,
        "featured_courses": featured_courses,
        "query": query,
    }

    return render(
        request,
        "courses/courses.html",
        context
    )




def add_new_course(request):

    if request.method == "POST":

        title = request.POST.get("title", "").strip()
        link = request.POST.get("link", "").strip()
        thumbnail = request.FILES.get("thumbnail")

        if not title:

            return render(
                request,
                "courses/add_new_course.html",
                {
                    "error": "يرجى إدخال عنوان الدورة.",
                    "title": title,
                    "link": link,
                }
            )


        # التحقق من الرابط
        if not link:

            return render(
                request,
                "courses/add_new_course.html",
                {
                    "error": "يرجى إدخال رابط الدورة.",
                    "title": title,
                    "link": link,
                }
            )


        # التحقق من الصورة
        if not thumbnail:

            return render(
                request,
                "courses/add_new_course.html",
                {
                    "error": "يرجى اختيار صورة للدورة.",
                    "title": title,
                    "link": link,
                }
            )


        # إنشاء الدورة
        Course.objects.create(
            title=title,
            link=link,
            thumbnail=thumbnail,
            is_active=True
        )


        # رسالة نجاح
        messages.success(
            request,
            "تم إضافة الدورة بنجاح"
        )


        # POST -> Redirect -> GET
        return redirect("add_new_course")


    return render(
        request,
        "courses/add_new_course.html"
    )


def view_course(request, course_id):

    course = get_object_or_404(
        Course,
        id=course_id,
        is_active=True
    )

    related_courses = (
        Course.objects
        .filter(is_active=True)
        .exclude(id=course.id)
        .order_by("-published_at")[:6]
    )

    context = {
        "course": course,
        "related_courses": related_courses,
    }

    return render(
        request,
        "courses/view_course.html",
        context
    )


def all_courses(request):

    query = request.GET.get("q", "").strip()

    courses_queryset = Course.objects.filter(
        is_active=True
    )

    if query:
        courses_queryset = courses_queryset.filter(
            Q(title__icontains=query)
        )

    courses_queryset = courses_queryset.order_by(
        "-published_at"
    )

    paginator = Paginator(
        courses_queryset,
        9
    )

    page_number = request.GET.get("page")

    courses = paginator.get_page(
        page_number
    )

    context = {
        "courses": courses,
        "query": query,
    }

    return render(
        request,
        "courses/all_courses.html",
        context
    )

