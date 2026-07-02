from django.db import models
from django.core.exceptions import ValidationError


# ============================================
# 1. نموذج التصنيفات (Categories)
# ============================================
class Category(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Category Name (English)",
    )
    name_ar = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Category Name (Arabic)",
    )

    icon_svg = models.TextField(blank=True, null=True)


    is_active = models.BooleanField(default=True) 
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"{self.name_ar} ({self.name})"

    def get_fields_count(self):
        """عدد المجالات المرتبطة بهذا التصنيف"""
        return self.fields.count()


class Field(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='fields',
        verbose_name="Category related to this field",
    )
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Field Name (English)",
    )
    name_ar = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Field Name (Arabic)",
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Field Description",
    )
    is_active = models.BooleanField(default=True)  # ❌ كانت False
    order = models.PositiveIntegerField(default=0)
    is_other = models.BooleanField(default=False)

    class Meta:
        ordering = ['category__order', 'order', 'name']
        unique_together = ['category', 'name']
        verbose_name = "Field"
        verbose_name_plural = "Fields"

    def __str__(self):
        return f"{self.name_ar} ({self.category.name_ar})"

    def clean(self):
        if self.is_other:
            existing_other = Field.objects.filter(
                category=self.category,
                is_other=True
            ).exclude(id=self.id)
            if existing_other.exists():
                raise ValidationError(
                    f"يوجد بالفعل خيار 'أخرى' في تصنيف {self.category.name_ar}"
                )


class Courses(models.Model):
    # تعريف خيارات المستوى
    LEVEL_CHOICES = [
        ("Beginner", "مبتدئ"),
        ("Intermediate", "متوسط"),
        ("Advanced", "متقدم"),
    ]

    # ------------------------ المعلومات الأساسية ------------------------
    title = models.CharField(max_length=200, verbose_name="Course Title")
    teacher_name = models.CharField(max_length=100, verbose_name="Teacher Name")
    channel_name = models.CharField(max_length=100, blank=True, verbose_name="Channel Name")

    # ------------------------ التصنيفات (مرتبطة بقاعدة البيانات) ------------------------
    # ✅ التعديل: استخدام ForeignKey بدلاً من CharField
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,  # إذا حذف التصنيف، يبقى الكورس بدون تصنيف
        null=True,
        blank=True,
        related_name='courses',
        verbose_name="Category"
    )
    
    field = models.ForeignKey(
        Field,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='courses',
        verbose_name="Field"
    )

    # ------------------------ تفاصيل الكورس ------------------------
    language = models.CharField(max_length=50, verbose_name="Language")
    duration = models.CharField(max_length=50, verbose_name="Duration")
    description = models.TextField(verbose_name="Description")
    link = models.URLField(unique=True, verbose_name="Course Link")

    thumbnail = models.ImageField(
        upload_to="courses/",
        blank=True,
        null=True,
        verbose_name="Thumbnail"
    )

    level = models.CharField(
        max_length=20,
        choices=LEVEL_CHOICES,
        default="Beginner",
        verbose_name="Level"
    )

    is_free = models.BooleanField(default=True, verbose_name="Is Free?")
    certificate = models.BooleanField(default=False, verbose_name="Has Certificate?")
    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=0.0,
        verbose_name="Rating"
    )
    status = models.BooleanField(default=True, verbose_name="Active")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_category_name(self):
        """إرجاع اسم التصنيف بالعربية"""
        return self.category.name_ar if self.category else "غير مصنف"
    get_category_name.short_description = "Category"

    def get_field_name(self):
        """إرجاع اسم المجال بالعربية"""
        return self.field.name_ar if self.field else "غير محدد"
    get_field_name.short_description = "Field"