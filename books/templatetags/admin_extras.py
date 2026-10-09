from django import template

register = template.Library()


@register.filter
def fa_digits(value):
    """تبدیل ارقام انگلیسی به فارسی"""
    return str(value).translate(str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹"))
