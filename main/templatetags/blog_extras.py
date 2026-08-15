import bleach
import calendar
import jdatetime
from zoneinfo import ZoneInfo

from django import template
from django.utils import timezone
from django.utils.translation import get_language
from django.utils.safestring import mark_safe


register = template.Library()

PERSIAN_MONTH_NAMES = (
    "",
    "فروردین",
    "اردیبهشت",
    "خرداد",
    "تیر",
    "مرداد",
    "شهریور",
    "مهر",
    "آبان",
    "آذر",
    "دی",
    "بهمن",
    "اسفند",
)
PERSIAN_DIGIT_TRANSLATION = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")
TEHRAN_TIME_ZONE = ZoneInfo("Asia/Tehran")

ALLOWED_TAGS = {
    "a",
    "blockquote",
    "br",
    "code",
    "figcaption",
    "figure",
    "h2",
    "h3",
    "h4",
    "hr",
    "img",
    "li",
    "ol",
    "p",
    "pre",
    "strong",
    "em",
    "table",
    "tbody",
    "td",
    "th",
    "thead",
    "tr",
    "ul",
}

ALLOWED_ATTRIBUTES = {
    "a": ["href", "title", "target", "rel"],
    "figure": ["class"],
    "figcaption": ["class"],
    "img": ["src", "alt", "width", "height", "class"],
    "table": ["class"],
    "td": ["colspan", "rowspan"],
    "th": ["colspan", "rowspan", "scope"],
}


@register.filter(name="safe_blog_html")
def safe_blog_html(value):
    cleaned_html = bleach.clean(
        value or "",
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        protocols={"http", "https", "mailto", "tel"},
        strip=True,
    )
    cleaned_html = bleach.linkify(cleaned_html)
    return mark_safe(cleaned_html)


def _to_jalali(value):
    if not value:
        return None
    if timezone.is_aware(value):
        value = timezone.localtime(value, TEHRAN_TIME_ZONE)
    return jdatetime.datetime.fromgregorian(datetime=value)


def _persian_number(value):
    return str(value).translate(PERSIAN_DIGIT_TRANSLATION)


@register.filter(name="jalali_date_parts")
def jalali_date_parts(value):
    jalali_value = _to_jalali(value)
    if not jalali_value:
        return {"day": "", "month": "", "year": ""}
    return {
        "day": _persian_number(jalali_value.day),
        "month": PERSIAN_MONTH_NAMES[jalali_value.month],
        "year": _persian_number(jalali_value.year),
    }


@register.filter(name="jalali_date")
def jalali_date(value):
    jalali_value = _to_jalali(value)
    if not jalali_value:
        return ""
    return _persian_number(
        f"{jalali_value.year:04d}/{jalali_value.month:02d}/{jalali_value.day:02d}"
    )


@register.filter(name="localized_date_parts")
def localized_date_parts(value):
    if get_language() != "en":
        return jalali_date_parts(value)
    if not value:
        return {"day": "", "month": "", "year": ""}
    if timezone.is_aware(value):
        value = timezone.localtime(value, TEHRAN_TIME_ZONE)
    return {
        "day": str(value.day),
        "month": calendar.month_name[value.month],
        "year": str(value.year),
    }


@register.filter(name="localized_date")
def localized_date(value):
    if get_language() != "en":
        return jalali_date(value)
    if not value:
        return ""
    if timezone.is_aware(value):
        value = timezone.localtime(value, TEHRAN_TIME_ZONE)
    return value.strftime("%Y/%m/%d")
