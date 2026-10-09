from django.contrib.auth.apps import AuthConfig as DjangoAuthConfig


class EnglishAuthConfig(DjangoAuthConfig):
    """برای نمایش نام انگلیسی «Authentication and Authorization» در ادمین"""
    verbose_name = "Authentication and Authorization"
