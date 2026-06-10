from django.db import models


# Create your models here.


class Quotes(models.Model):
    text = models.TextField()
    author = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'"{self.text}" - {self.author}'

    class Meta:
        app_label = 'ZadTech'  # <-- CRITICAL: Must match your project folder name
