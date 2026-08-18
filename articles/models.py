from django.db import models


class Article(models.Model):

    title = models.CharField(
        max_length=255,
        verbose_name="عنوان المقال"
    )

    description = models.TextField(
        verbose_name="محتوى المقال"
    )

    image = models.ImageField(
        upload_to="articles/images/",
        blank=True,
        null=True,
        verbose_name="صورة المقال"
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
        verbose_name = "مقال"
        verbose_name_plural = "المقالات"
        ordering = ["-published_at"]

