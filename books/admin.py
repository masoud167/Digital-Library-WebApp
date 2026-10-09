from django.contrib import admin
from .models import Category, Book, BookImage, BorrowRecord, Review

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent')
    list_select_related = ('parent',)
    prepopulated_fields = {'slug': ('name',)}  # ساخت خودکار slug از روی نام

class BookImageInline(admin.TabularInline):
    """افزودن چند تصویر برای هر کتاب در همان صفحه ویرایش کتاب"""
    model = BookImage
    extra = 3
    min_num = 0

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'published_year', 'created_at')
    list_filter = ('category', 'published_year')
    search_fields = ('title', 'author', 'description')
    inlines = [BookImageInline]

@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'borrow_date', 'return_date')
    list_filter = ('borrow_date',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('book__title', 'user__username', 'comment')