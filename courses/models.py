from django.db import models


class Course(models.Model):

    title = models.CharField(
        max_length=255,
        verbose_name="عنوان الدورة"
    )

    link = models.URLField(
        max_length=500,
        verbose_name="رابط الدورة"
    )

    thumbnail = models.ImageField(
        upload_to="courses/thumbnail/",
        verbose_name="الصورة المصغرة"
    )

    is_active = models.BooleanField(
        default=False,
        verbose_name="فعال"
    )

    published_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاريخ النشر"
    )


    def __str__(self):
        return self.title


    class Meta:
        verbose_name = "دورة"
        verbose_name_plural = "الدورات"
        ordering = ["-published_at"]
