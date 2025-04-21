from django.contrib import admin
from .models import Category, Blogs, Comment

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name', 'created_at', 'updated_at')

class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'author', 'blog_image', 'status', 'is_featured', 'created_at', 'updated_at')  # Corrected field name
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('id', 'title', 'category__category_name', 'status')
    list_editable = ('is_featured',)  # Corrected field name

admin.site.register(Category, CategoryAdmin)
admin.site.register(Blogs, BlogAdmin)
admin.site.register(Comment)
