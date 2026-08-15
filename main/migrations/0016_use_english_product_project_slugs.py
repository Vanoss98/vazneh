from django.db import migrations
from django.utils.text import slugify


def update_slugs(model, title_field, fallback, allow_unicode):
    objects = list(model.objects.order_by("pk"))

    for item in objects:
        model.objects.filter(pk=item.pk).update(
            slug=f"migration-temp-{fallback}-{item.pk}"
        )

    used_slugs = set()
    for item in objects:
        title = getattr(item, title_field, "") or item.title
        base_slug = slugify(title, allow_unicode=allow_unicode) or fallback
        candidate = base_slug[:200]
        suffix = 2
        while candidate in used_slugs:
            suffix_text = f"-{suffix}"
            candidate = f"{base_slug[:200 - len(suffix_text)]}{suffix_text}"
            suffix += 1
        used_slugs.add(candidate)
        model.objects.filter(pk=item.pk).update(slug=candidate)


def use_english_slugs(apps, schema_editor):
    update_slugs(apps.get_model("main", "Product"), "title_en", "product", False)
    update_slugs(apps.get_model("main", "Project"), "title_en", "project", False)


def restore_persian_slugs(apps, schema_editor):
    update_slugs(apps.get_model("main", "Product"), "title", "product", True)
    update_slugs(apps.get_model("main", "Project"), "title", "project", True)


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0015_populate_english_content"),
    ]

    operations = [
        migrations.RunPython(use_english_slugs, restore_persian_slugs),
    ]
