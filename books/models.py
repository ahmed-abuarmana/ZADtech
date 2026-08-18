from pathlib import Path
import logging
import pymupdf

from django.db import models
from django.core.files.base import ContentFile


logger = logging.getLogger(__name__)


class Book(models.Model):

    title = models.CharField(
        max_length=255,
        verbose_name="عنوان الكتاب"
    )

    description = models.TextField(
        verbose_name="وصف الكتاب"
    )

    book_file = models.FileField(
        upload_to="books/",
        verbose_name="ملف الكتاب"
    )

    # صورة الغلاف المستخرجة من الصفحة الأولى
    cover_image = models.FileField(
        upload_to="books/covers/",
        blank=True,
        null=True,
        editable=False,
        verbose_name="صورة الغلاف"
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="فعال"
    )

    published_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاريخ النشر"
    )


    def __str__(self):
        return self.title


    def generate_cover(self, force=False):
        """
        إنشاء صورة PNG من الصفحة الأولى لملف PDF.
        """

        if not self.book_file:
            return False

        # إذا كانت الصورة موجودة بالفعل فلا نعيد إنشاءها
        if self.cover_image and not force:
            return True

        try:

            # قراءة ملف PDF
            self.book_file.open("rb")

            try:
                pdf_bytes = self.book_file.read()
            finally:
                self.book_file.close()


            # فتح PDF من الذاكرة
            document = pymupdf.open(
                stream=pdf_bytes,
                filetype="pdf"
            )


            try:

                # التأكد من وجود صفحة واحدة على الأقل
                if document.page_count == 0:
                    return False


                # الصفحة الأولى رقمها 0
                page = document.load_page(0)


                # تحويل الصفحة إلى صورة
                pixmap = page.get_pixmap(
                    dpi=150,
                    alpha=False
                )


                # تحويل الصورة إلى PNG bytes
                image_bytes = pixmap.tobytes("png")


            finally:
                document.close()


            # اسم الصورة
            pdf_name = Path(self.book_file.name).stem

            cover_name = f"{pdf_name}_cover.png"


            # إذا طلبنا إعادة إنشاء الصورة
            if force and self.cover_image:
                self.cover_image.delete(save=False)


            # حفظ الصورة داخل media/books/covers/
            self.cover_image.save(
                cover_name,
                ContentFile(image_bytes),
                save=False
            )


            # تحديث حقل الصورة فقط
            self.save(
                update_fields=["cover_image"]
            )


            return True


        except Exception:

            logger.exception(
                "Failed to generate cover for book ID %s",
                self.pk
            )

            return False


    class Meta:
        verbose_name = "كتاب"
        verbose_name_plural = "الكتب"
        ordering = ["-published_at"]
        