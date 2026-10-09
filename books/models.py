from django.db import models
from django.contrib.auth.models import User

#  مدل دسته‌بندی کتاب‌ها
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام دسته‌بندی")
    slug = models.SlugField(unique=True, verbose_name="شناسه یکتا (Slug)")
    parent = models.ForeignKey(
        'self',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='children',
        verbose_name="دسته والد",
        help_text="در صورت خالی‌بودن، این دسته یک دسته اصلی است",
    )

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"

    def __str__(self):
        return self.name

#  مدل کتاب
class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان کتاب")
    author = models.CharField(max_length=150, verbose_name="نویسنده")
    description = models.TextField(verbose_name="توضیحات / خلاصه")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='books', verbose_name="دسته‌بندی")
    
    # فایل‌ها
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True, verbose_name="تصویر جلد")
    pdf_file = models.FileField(upload_to='books_pdf/', verbose_name="فایل PDF")
    
    published_year = models.IntegerField(verbose_name="سال انتشار", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ افزودن")

    class Meta:
        verbose_name = "کتاب"
        verbose_name_plural = "کتاب‌ها"

    def __str__(self):
        return self.title

#  مدل دانلود کتاب
class BorrowRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='borrowed_books', verbose_name="کاربر")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrowed_by', verbose_name="کتاب")
    borrow_date = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ دریافت")
    return_date = models.DateTimeField(null=True, blank=True, verbose_name="تاریخ بازگرداندن")

    class Meta:
        verbose_name = "سابقه امانت"
        verbose_name_plural = "سوابق امانت"

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"


#  مدل تصاویر گالری کتاب (چند تصویر برای هر کتاب؛ کتاب بدون تصویر هم قابل ثبت است)
class BookImage(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='images', verbose_name="کتاب")
    image = models.ImageField(upload_to='book_gallery/', verbose_name="تصویر")
    caption = models.CharField(max_length=200, blank=True, verbose_name="توضیح تصویر")

    class Meta:
        verbose_name = "تصویر کتاب"
        verbose_name_plural = "تصاویر کتاب"
        ordering = ('id',)

    def __str__(self):
        return f"تصویر {self.book.title}"


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews', verbose_name="کتاب")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', verbose_name="کاربر")
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], verbose_name="امتیاز (از ۵)")
    comment = models.TextField(verbose_name="متن نظر")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")

    class Meta:
        verbose_name = "نظر"
        verbose_name_plural = "نظرات"
        # هر کاربر فقط یک بار می‌تواند برای هر کتاب نظر ثبت کند (اختیاری)
        unique_together = ('book', 'user')

    def __str__(self):
        return f"{self.user.username} بر روی {self.book.title} - امتیاز: {self.rating}"




