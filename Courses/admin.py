from django.contrib import admin
from .models import Category, Field, Courses


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name_ar', 'name', 'is_active', 'order', 'get_fields_count']
    list_editable = ['is_active', 'order']
    search_fields = ['name', 'name_ar']
    
    def get_fields_count(self, obj):
        return obj.fields.count()
    get_fields_count.short_description = "عدد المجالات"

    


@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    list_display = ['name_ar', 'name', 'category', 'is_active', 'is_other', 'order']
    list_editable = ['is_active', 'is_other', 'order']
    search_fields = ['name', 'name_ar', 'category__name_ar']
    list_filter = ['category', 'is_active', 'is_other']


@admin.register(Courses)
class CoursesAdmin(admin.ModelAdmin):
    # ✅ تأكد من وجود جميع الحقول في list_display
    list_display = [
        'title', 
        'get_category_name', 
        'get_field_name', 
        'teacher_name', 
        'level', 
        'is_free', 
        'certificate', 
        'rating',
        'status' 
    ]
    
    list_filter = ['level', 'is_free', 'certificate', 'status']
    search_fields = ['title', 'teacher_name', 'description']
    autocomplete_fields = ['category', 'field']
    
    # ✅ الآن جميع الحقول موجودة في list_display
    list_editable = ['level', 'is_free', 'certificate', 'rating', 'status']
    
    def get_category_name(self, obj):
        return obj.category.name_ar if obj.category else "-"
    get_category_name.short_description = "التصنيف"
    
    def get_field_name(self, obj):
        return obj.field.name_ar if obj.field else "-"
    get_field_name.short_description = "المجال"