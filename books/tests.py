import shutil
import tempfile

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Book, Category, BorrowRecord, Review

TINY_PDF = (
    b"%PDF-1.4\n"
    b"1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n"
    b"2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n"
    b"3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]>>endobj\n"
    b"trailer<</Root 1 0 R>>\n"
    b"%%EOF\n"
)

TEST_MEDIA_ROOT = tempfile.mkdtemp(prefix="digital_lib_test_media_")


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class BookFlowTests(TestCase):
    """آزمون‌های خودکار جریان اصلی کتابخانه دیجیتال"""

    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name="رایانه", slug="computer")
        cls.book = Book.objects.create(
            title="پایتون در یک ساعت",
            author="Stephen Somebody",
            description="کتاب نمونه برای آزمون",
            category=cls.category,
            published_year=1403,
            pdf_file=SimpleUploadedFile(
                "sample.pdf", TINY_PDF, content_type="application/pdf"
            ),
        )
        cls.member = User.objects.create_user(username="ali", password="StrongPass123")
        cls.other_member = User.objects.create_user(
            username="sara", password="StrongPass123"
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEST_MEDIA_ROOT, ignore_errors=True)


    def test_01_wrong_password_login_fails(self):
        logged_in = self.client.login(username="ali", password="wrong-password")
        self.assertFalse(logged_in)

    def test_02_guest_cannot_borrow(self):
        url = reverse("books:borrow_book", args=[self.book.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("accounts:login"), response["Location"])
        self.assertEqual(BorrowRecord.objects.count(), 0)

    def test_03_guest_cannot_download(self):
        url = reverse("books:download_book", args=[self.book.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("accounts:login"), response["Location"])

    def test_04_member_without_record_gets_404_on_download(self):
        self.client.login(username="sara", password="StrongPass123")
        url = reverse("books:download_book", args=[self.book.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_05_guest_cannot_post_review(self):
        url = reverse("books:book_detail", args=[self.book.pk])
        response = self.client.post(url, {"rating": 5, "comment": "خوب بود"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Review.objects.count(), 0)

    def test_06_member_borrow_returns_pdf_and_creates_record(self):
        self.client.login(username="ali", password="StrongPass123")
        url = reverse("books:borrow_book", args=[self.book.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("application/pdf", response["Content-Type"])
        self.assertTrue(response.streaming)
        body = b"".join(response.streaming_content)
        self.assertTrue(body.startswith(b"%PDF"))
        records = BorrowRecord.objects.filter(user=self.member, book=self.book)
        self.assertEqual(records.count(), 1)

    def test_07_duplicate_borrow_keeps_single_record(self):
        self.client.login(username="ali", password="StrongPass123")
        url = reverse("books:borrow_book", args=[self.book.pk])
        self.client.get(url)
        self.client.get(url)
        self.client.get(url)
        records = BorrowRecord.objects.filter(user=self.member, book=self.book)
        self.assertEqual(records.count(), 1)

    def test_08_member_with_record_can_redownload(self):
        self.client.login(username="ali", password="StrongPass123")
        self.client.get(reverse("books:borrow_book", args=[self.book.pk]))
        response = self.client.get(
            reverse("books:download_book", args=[self.book.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("application/pdf", response["Content-Type"])

    def test_09_duplicate_review_updates_existing(self):
        self.client.login(username="ali", password="StrongPass123")
        url = reverse("books:book_detail", args=[self.book.pk])
        self.client.post(url, {"rating": 4, "comment": "نظر اول"})
        self.client.post(url, {"rating": 2, "comment": "نظر دوم"})
        reviews = Review.objects.filter(user=self.member, book=self.book)
        self.assertEqual(reviews.count(), 1)
        self.assertEqual(reviews.first().rating, 2)
        self.assertEqual(reviews.first().comment, "نظر دوم")


class SearchAndFilterTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.cat_computer = Category.objects.create(name="رایانه", slug="computer")
        cls.cat_literature = Category.objects.create(name="ادبی", slug="literature")
        cls.book_python = Book.objects.create(
            title="Learning Python",
            author="Mark Lutz",
            description="",
            category=cls.cat_computer,
        )
        cls.book_shahnameh = Book.objects.create(
            title="شاهنامه فردوسی",
            author="فردوسی",
            description="",
            category=cls.cat_literature,
        )

    def test_10_search_is_case_insensitive(self):
        response = self.client.get("/", {"q": "learning PYTHON"})
        self.assertEqual(response.status_code, 200)
        results = list(response.context["books"])
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].pk, self.book_python.pk)

    def test_11_search_by_author(self):
        response = self.client.get("/", {"q": "فردوسی"})
        results = list(response.context["books"])
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].pk, self.book_shahnameh.pk)

    def test_12_category_filter(self):
        response = self.client.get("/", {"category": "literature"})
        results = list(response.context["books"])
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].pk, self.book_shahnameh.pk)
