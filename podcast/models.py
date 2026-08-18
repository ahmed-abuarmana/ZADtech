from django.db import models


class Podcast(models.Model):

    title = models.CharField(
        max_length=255,
        verbose_name="عنوان البودكاست"
    )

    youtube_url = models.URLField(
        max_length=500,
        verbose_name="رابط البودكاست على يوتيوب"
    )

    image = models.ImageField(
        upload_to="podcast/images/",
        blank=True,
        null=True,
        verbose_name="صورة البودكاست"
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

    class Meta:
        verbose_name = "بودكاست"
        verbose_name_plural = "البودكاست"
        ordering = ["-published_at"]
