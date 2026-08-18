from django.shortcuts import render, redirect, get_object_or_404
from .models import Book
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator




def book_list(request):

    # الحصول على كلمة البحث
    query = request.GET.get('q', '').strip()

    # جلب الكتب الفعالة فقط
    books_queryset = Book.objects.filter(
        is_active=True
    )

    # البحث في العنوان أو الوصف
    if query:
        books_queryset = books_queryset.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )

    # ترتيب الكتب من الأحدث إلى الأقدم
    books_queryset = books_queryset.order_by(
        '-published_at'
    )

    # 6 كتب في كل صفحة
    paginator = Paginator(
        books_queryset,
        6
    )

    page_number = request.GET.get('page')

    books = paginator.get_page(
        page_number
    )

    # تقسيم الكتب إلى نفس القسمين الموجودين في التصميم الأصلي
    current_books = list(books.object_list)

    first_books = current_books[:3]
    second_books = current_books[3:]

    context = {
        'books': books,
        'first_books': first_books,
        'second_books': second_books,
        'query': query,
    }

    return render(
        request,
        'books/books.html',
        context
    )


def view_book(request, book_id):

    book = get_object_or_404(
        Book,
        id=book_id,
        is_active=True
    )

    related_books = (
        Book.objects
        .filter(is_active=True)
        .exclude(id=book.id)
        .order_by("-published_at")[:5]
    )

    context = {
        "book": book,
        "related_books": related_books,
    }

    return render(
        request,
        "books/view_book.html",
        context
    )


def add_new_book(request):

    if request.method == "POST":

        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        book_file = request.FILES.get("book_file")


        if not title:

            return render(
                request,
                "books/add_new_book.html",
                {
                    "error": "يرجى إدخال عنوان الكتاب.",
                    "title": title,
                    "description": description,
                }
            )


        if not description:

            return render(
                request,
                "books/add_new_book.html",
                {
                    "error": "يرجى إدخال وصف الكتاب.",
                    "title": title,
                    "description": description,
                }
            )



        if not book_file:

            return render(
                request,
                "books/add_new_book.html",
                {
                    "error": "يرجى اختيار ملف الكتاب.",
                    "title": title,
                    "description": description,
                }
            )

        book = Book.objects.create(
            title=title,
            description=description,
            book_file=book_file,
            is_active=True
        )

        # إنشاء صورة الغلاف من أول صفحة PDF
        book.generate_cover()


        messages.success(
            request,
            "تم نشر الكتاب بنجاح"
        )

        return redirect("add_new_book")


    return render(
        request,
        "books/add_new_book.html"
    )