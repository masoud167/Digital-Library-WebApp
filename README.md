<div dir="rtl">

# 📚 وب‌گاه کتابخانه دیجیتال | Digital Library WebApp

پروژهٔ کارشناسی «طراحی و پیاده‌سازی وب‌گاه کتابخانه دیجیتال» — سامانه‌ای سبک، رایگان و فارسی (RTL) بر بستر جنگو، برای کتابخانه‌های کوچک و متوسط.

[**فارسی**](#fa) | [**English**](#en)

![Django](https://img.shields.io/badge/Django-5.2.8-092E20)
![Python](https://img.shields.io/badge/Python-3.10.10-3776AB)
![Tests](https://img.shields.io/badge/tests-12%2F12%20passed-brightgreen)
![UI](https://img.shields.io/badge/UI-Persian%20RTL-blue)

<a id="fa"></a>

---

## ✨ معرفی

این سامانه چرخهٔ کامل امانت دیجیتال یک کتابخانه را پوشش می‌دهد: کاربر پس از ثبت‌نام می‌تواند کتاب‌ها را جستجو و فیلتر کند، جزئیات و نظرات را ببیند، کتاب را امانت بگیرد، فایل PDF را دریافت و بارها دوباره دانلود کند، نظر بگذارد و سوابقش را در پروفایل شخصی ببیند؛ مدیر نیز محتوا را از پنل مدیریت جنگو مدیریت می‌کند.

ویژگی‌های برجسته:

- **جستجوی هوشمند**: جستجوی غیرحساس به حروف روی عنوان و نویسنده
- **فیلتر چنددسته‌ای**: انتخاب هم‌زمان چند دسته به‌همراه زیردسته‌ها (پیمایش درختی)
- **نظر یکتا**: هر کاربر برای هر کتاب فقط یک نظر فعال دارد (به‌روزرسانی با `update_or_create` + قید `unique_together`)
- **امانت بدون رکورد تکراری**: ثبت سابقه با `get_or_create`؛ کلیک‌های پشت‌سرهم رکورد دوم نمی‌سازند
- **سرو امن فایل PDF**: پاسخ مستقیم با `FileResponse`؛ دریافت فقط برای دارندگان سابقهٔ امانت، وگرنه خطای ۴۰۴
- **پنل مدیریت فارسی راست‌چین** با پوستهٔ تیرهٔ سفارشی و دکمهٔ بازگشت در صفحات داخلی
- **رابط کاملاً فارسی و RTL** در همهٔ قالب‌ها

## 🛠 فناوری‌ها

| لایه | فناوری |
|---|---|
| زبان | Python 3.10 |
| فریمورک | Django 5.2.8 (الگوی MVT) |
| پایگاه داده | SQLite (بدون نیاز به سرور جداگانه) |
| مدیریت تصویر | Pillow |
| رابط کاربری | HTML/CSS سفارشی، راست‌چین |

## 🚀 راه‌اندازی

```bash
# ۱) دریافت مخزن
git clone https://github.com/masoud167/Digital-Library-WebApp.git
cd Digital-Library-WebApp

# ۲) ساخت محیط مجازی و نصب وابستگی‌ها
python -m venv venv
venv\Scripts\activate          # در لینوکس/مک:  source venv/bin/activate
pip install -r requirements.txt

# ۳) آماده‌سازی پایگاه داده
python manage.py migrate
python manage.py createsuperuser   # برای ورود به پنل مدیریت

# ۴) اجرا
python manage.py runserver
```

- نشانی سامانه: <http://127.0.0.1:8000/>
- پنل مدیریت: <http://127.0.0.1:8000/admin/>

> **نکته:** فایل‌های `media/` (جلدها و PDFها) و `db.sqlite3` عمداً در مخزن نیستند؛ پس از اجرا، داده‌های نمونه را از طریق پنل ادمین اضافه کنید.

## 🧪 آزمون‌ها

```bash
python manage.py test
```

**۱۲ آزمون خودکار، همگی سبز** — نام متد‌ها (`test_01` … `test_12`) با شناسه‌های `T-01` … `T-12` گزارش پروژه یکی است:

| آزمون | نوع | آنچه اثبات می‌کند |
|---|---|---|
| test_01 / T-01 | منفی | ورود با رمز نادرست ناموفق است و جلسه‌ای ساخته نمی‌شود |
| test_02 / T-02 | منفی | امانتِ کاربر مهمان → هدایت به ورود، صفر رکورد |
| test_03 / T-03 | منفی | دانلودِ کاربر مهمان → هدایت به ورود |
| test_04 / T-04 | منفی | عضوِ بدون سابقهٔ امانت → خطای ۴۰۴ |
| test_05 / T-05 | منفی | ثبت نظرِ مهمان → هدایت به ورود، صفر نظر |
| test_06 / T-06 | مثبت | امانت عضو: پاسخ PDF + دقیقاً یک رکورد |
| test_07 / T-07 | مثبت | امانت تکراریِ سه‌باره → همچنان یک رکورد |
| test_08 / T-08 | مثبت | دانلود مجددِ دارندهٔ سابقه → ۲۰۰ با PDF |
| test_09 / T-09 | مثبت | نظر دوم همان کاربر نظر قبلی را به‌روزرسانی می‌کند |
| test_10 / T-10 | مثبت | جستجوی غیرحساس به حروف |
| test_11 / T-11 | مثبت | جستجو با نام نویسنده |
| test_12 / T-12 | مثبت | فیلتر دسته‌بندی فقط کتاب‌های همان دسته را نشان می‌دهد |

آزمون‌ها در دیتابیس درون‌حافظه‌ای جداگانه اجرا می‌شوند و فایل‌های آزمون در پوشهٔ موقت جدا از `media` واقعی ساخته می‌شوند؛ بنابراین اجرای دوباره هیچ داده‌ای را تغییر نمی‌دهد.

## 🗂 ساختار پروژه

```
Digital-Library-WebApp/
├── manage.py
├── requirements.txt
├── .gitignore
├── digital_lib/                 # تنظیمات پروژه
│   ├── settings.py              # اپ‌ها، میان‌افزارها، مسیرها
│   ├── urls.py                  # مسیردهی ریشه (admin + books)
│   └── apps.py                  # نام انگلیسی برای اپ استاندارد auth
├── books/                       # اپ محتوا و فرایند امانت
│   ├── models.py                # Category, Book, BorrowRecord, BookImage, Review
│   ├── views.py                 # فهرست/جزئیات/امانت/دانلود
│   ├── urls.py                  # فضای نام books
│   ├── admin.py                 # ثبت مدل‌ها و inline گالری
│   ├── tests.py                 # ۱۲ آزمون خودکار
│   ├── templatetags/admin_extras.py
│   ├── migrations/
│   └── templates/books/         # قالب فهرست و جزئیات
├── accounts/                    # اپ هویت کاربران
│   ├── views.py                 # ثبت‌نام، ورود/خروج، پروفایل
│   ├── urls.py                  # فضای نام accounts
│   └── templates/accounts/      # قالب‌های ورود/ثبت‌نام/پروفایل
├── templates/admin/             # بازنویسی قالب‌های ادمین (عنوان‌های غیرلینک و…)
└── static/admin_custom/         # پوستهٔ فارسی تیرهٔ پنل مدیریت (admin.css)
```

## 🗺 مسیرهای اصلی

| مسیر | توضیح | احراز هویت |
|---|---|---|
| `/` | فهرست کتاب‌ها + جستجو + فیلتر چنددسته‌ای | — |
| `/book/<id>/` | جزئیات کتاب، گالری، نظرات | ثبت نظر: عضو |
| `/book/<id>/borrow/` | ثبت سابقهٔ امانت + دریافت فایل PDF | الزامی |
| `/book/<id>/download/` | دانلود مجدد فایل | الزامی + سابقهٔ امانت |
| `/accounts/signup/` | ثبت‌نام (اعتبارسنج‌های رمز جنگو) | — |
| `/accounts/login/` · `/accounts/logout/` | ورود / خروج (POST) | — |
| `/accounts/profile/` | سوابق امانت و دانلود مجدد | الزامی |
| `/admin/` | پنل مدیریت محتوا | مدیر |

## 📈 معماری و طراحی

- الگوی **MVT** جنگو؛ دو اپ `books` و `accounts` با فضای‌نام مجزا
- پنج مدل داده‌ای با `verbose_name` فارسی؛ رابطهٔ خودارجاعی `Category.parent` برای زیردسته‌ها
- کنترل دسترسی دولایه: شرط در قالب (تجربهٔ کاربری) + کنترل در ویو (`@login_required`، بررسی سابقه) — لایهٔ امنیتی، لایهٔ ویو است
- سرو فایل از ویو با `FileResponse`؛ آدرس فایل هرگز به مرورگر لو نمی‌رود
- پوستهٔ ادمین با CSS سفارشی روی قالب‌های استاندارد جنگو (بدون تغییر هسته)

## ⚠️ محدودیت‌های شناخته‌شده

- بدون صفحه‌بندی (Pagination) در فهرست کتاب‌ها — با رشد مجموعه، افزوده شود
- بدون سقف حجم برای آپلود PDF در کد (سقف باید در سرور استقرار تعیین شود)
- `runserver` صرفاً برای توسعه است؛ استقرار باید با WSGI + وب‌سرور (nginx/Gunicorn) انجام شود
- در حالت توسعه، فایل‌های `media` مستقیماً سرو می‌شوند (در استقرار باید محافظت شوند)
- بدون آزمون پوشش کد (coverage)، آزمون بار و آزمون مرورگر واقعی

## 📄 گزارش پروژه

مستندسازی کامل تحلیل، طراحی (نیازمندی‌ها، قواعد کسب‌وکار، ER، نمودارهای تحلیلی)، پیاده‌سازی و آزمون در **گزارشکار نهایی** پروژه (فایل Word/PDF) موجود است. کد این مخزن همان کدی است که در گزارش مستند شده و ۱۲ آزمون آن با جدول‌های آزمون گزارش یکی است.

## 🔗 مراجع

- [مستندات جنگو ۵.۲](https://docs.djangoproject.com/5.2/)
- [جنگو: امنیت](https://docs.djangoproject.com/5.2/topics/security/)
- [جنگو: چارچوب تست](https://docs.djangoproject.com/5.2/topics/testing/)

**نویسنده:** محمد مسعود تقی‌پور — `masoud167`

</div>

<a id="en"></a>

---

# 📚 Digital Library WebApp

Bachelor's project: *Design and Implementation of a Digital Library Website* — a lightweight, free, Persian-first (RTL) digital library system built with Django for small and medium libraries.

[فارسی](#fa) | [**English**](#en)

![Django](https://img.shields.io/badge/Django-5.2.8-092E20)
![Python](https://img.shields.io/badge/Python-3.10.10-3776AB)
![Tests](https://img.shields.io/badge/tests-12%2F12%20passed-brightgreen)
![UI](https://img.shields.io/badge/UI-Persian%20RTL-blue)

## ✨ Overview

The system covers the full digital lending cycle of a library: after signing up, a user can search and filter books, view details and reviews, borrow a book, download the PDF and re-download it later, post a review, and see their borrowing history in a personal profile; managers manage content through the Django admin panel.

Highlights:

- **Smart search**: case-insensitive search over title and author
- **Multi-category filter**: select several categories at once, including subcategories (tree traversal)
- **Unique review**: one active review per user per book (`update_or_create` + `unique_together` constraint)
- **Duplicate-free lending**: lending records are created with `get_or_create`, so back-to-back clicks never create a second row
- **Secure PDF serving**: the file is streamed directly with `FileResponse`; download is granted only to holders of a lending record, otherwise HTTP 404
- **Persian RTL admin panel** with a custom dark theme and a back button on inner pages
- **Fully Persian RTL UI** across all templates

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10 |
| Framework | Django 5.2.8 (MVT pattern) |
| Database | SQLite (no separate database server needed) |
| Image handling | Pillow |
| UI | Custom HTML/CSS, right-to-left |

## 🚀 Setup

```bash
# 1) Clone the repository
git clone https://github.com/masoud167/Digital-Library-WebApp.git
cd Digital-Library-WebApp

# 2) Create a virtual environment and install dependencies
python -m venv venv
venv\Scripts\activate          # Linux/macOS:  source venv/bin/activate
pip install -r requirements.txt

# 3) Prepare the database
python manage.py migrate
python manage.py createsuperuser   # for the admin panel

# 4) Run
python manage.py runserver
```

- Application: <http://127.0.0.1:8000/>
- Admin panel: <http://127.0.0.1:8000/admin/>

> **Note:** `media/` (covers and PDFs) and `db.sqlite3` are intentionally excluded from the repository; after running, add your sample data through the admin panel.

## 🧪 Tests

```bash
python manage.py test
```

**12 automated tests, all green** — method names (`test_01` … `test_12`) match report identifiers `T-01` … `T-12`:

| Test | Type | What it proves |
|---|---|---|
| test_01 / T-01 | Negative | Login with a wrong password fails and no session is created |
| test_02 / T-02 | Negative | Guest borrowing → redirect to login, zero records |
| test_03 / T-03 | Negative | Guest download → redirect to login |
| test_04 / T-04 | Negative | Member without a lending record → HTTP 404 |
| test_05 / T-05 | Negative | Guest review post → redirect to login, zero reviews |
| test_06 / T-06 | Positive | Member borrow: PDF response + exactly one record |
| test_07 / T-07 | Positive | Three consecutive borrows → still a single record |
| test_08 / T-08 | Positive | Re-download by a record holder → 200 with PDF |
| test_09 / T-09 | Positive | Second review by the same user updates the first one |
| test_10 / T-10 | Positive | Case-insensitive search |
| test_11 / T-11 | Positive | Search by author name |
| test_12 / T-12 | Positive | Category filter returns only that category's books |

Tests run against a separate in-memory database, and test files are written to a temporary folder outside the real `media/`; re-running them never modifies project data.

## 🗂 Project Structure

```
Digital-Library-WebApp/
├── manage.py
├── requirements.txt
├── .gitignore
├── digital_lib/                 # project settings
│   ├── settings.py              # apps, middleware, paths
│   ├── urls.py                  # root URLconf (admin + books)
│   └── apps.py                  # English app label for the standard auth app
├── books/                       # content & lending app
│   ├── models.py                # Category, Book, BorrowRecord, BookImage, Review
│   ├── views.py                 # list / detail / borrow / download
│   ├── urls.py                  # books namespace
│   ├── admin.py                 # model registration + gallery inline
│   ├── tests.py                 # 12 automated tests
│   ├── templatetags/admin_extras.py
│   ├── migrations/
│   └── templates/books/         # list and detail templates
├── accounts/                    # identity app
│   ├── views.py                 # signup, login/logout, profile
│   ├── urls.py                  # accounts namespace
│   └── templates/accounts/      # login / signup / profile templates
├── templates/admin/             # admin template overrides (non-link titles, …)
└── static/admin_custom/         # custom dark Persian admin theme (admin.css)
```

## 🗺 Main Routes

| Route | Description | Auth |
|---|---|---|
| `/` | Book list + search + multi-category filter | — |
| `/book/<id>/` | Book detail, gallery, reviews | Reviews: member |
| `/book/<id>/borrow/` | Create lending record + receive the PDF | Required |
| `/book/<id>/download/` | Re-download the file | Required + lending record |
| `/accounts/signup/` | Registration (Django password validators) | — |
| `/accounts/login/` · `/accounts/logout/` | Login / logout (POST) | — |
| `/accounts/profile/` | Lending history and re-download | Required |
| `/admin/` | Content management panel | Admin |

## 📈 Architecture and Design

- Django **MVT** pattern; two apps, `books` and `accounts`, with separate namespaces
- Five data models with Persian `verbose_name`s; self-referential `Category.parent` for subcategories
- Two-layer access control: template condition (user experience) + view control (`@login_required`, record check) — the view layer is the security layer
- Files are served from the view with `FileResponse`; the file URL is never exposed to the browser
- Admin theme is a custom CSS on top of Django's standard templates (no core changes)

## ⚠️ Known Limitations

- No pagination on the book list — add `Paginator` as the collection grows
- No upload size limit for PDFs in code (enforce it at the deployment server)
- `runserver` is for development only; deploy with WSGI + a web server (nginx/Gunicorn)
- In development, `media/` files are served directly (must be protected in production)
- No code-coverage, load, or real-browser tests

## 📄 Project Report

Full documentation of analysis, design (requirements, business rules, ER diagrams, analytical diagrams), implementation, and testing is available in the final project report (Word/PDF). The code in this repository is exactly the code documented there, and its 12 tests match the report's test tables.

## 🔗 References

- [Django 5.2 documentation](https://docs.djangoproject.com/5.2/)
- [Django security](https://docs.djangoproject.com/5.2/topics/security/)
- [Django testing framework](https://docs.djangoproject.com/5.2/topics/testing/)

**Author:** Mohammad Masoud Taghipour — `masoud167`
