from django.db import models
from Courses.models import Field, Category

class Article(models.Model):

    title = models.CharField(max_length=200, default='مقالة جديدة')

    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    author_name = models.CharField(max_length=100)

    content = models.TextField()

    summary = models.TextField(blank=True, null=True, default="وصف عام وبسيط للمقال في جملة واحدة")

    image = models.ImageField(
        upload_to="articles/",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    status = models.BooleanField(default=False, verbose_name="Is Active?")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.author_name
