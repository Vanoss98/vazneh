from decimal import Decimal

from django.db import migrations


SAMPLE_PROJECTS = (
    {
        "slug": "پروژه-فولاد-مبارکه-اصفهان",
        "title": "پروژه فولاد مبارکه اصفهان",
        "subtitle": "طراحی و اجرای جرثقیل سقفی خط تولید",
        "description": (
            "طراحی، ساخت و نصب جرثقیل سقفی این مجموعه با توجه به چرخه کاری "
            "سنگین و الزامات ایمنی خط تولید انجام شد. تمامی مراحل مهندسی و "
            "راه‌اندازی توسط تیم وزنه اجرا شده است."
        ),
        "location": "اصفهان، مجتمع فولاد مبارکه",
        "latitude": Decimal("32.595278"),
        "longitude": Decimal("51.514722"),
        "features": ["ظرفیت باربری بالا", "کنترل از راه دور", "چرخه کاری سنگین"],
    },
    {
        "slug": "پروژه-سالن-صنعتی-تهران",
        "title": "پروژه سالن صنعتی تهران",
        "subtitle": "تأمین و نصب سامانه جابه‌جایی مواد",
        "description": (
            "برای این سالن صنعتی، سامانه کامل جابه‌جایی مواد از مرحله برداشت "
            "ابعاد تا نصب و تحویل نهایی طراحی شد. راهکار اجراشده فضای کاری ایمن "
            "و دسترسی سریع‌تر به خطوط تولید را فراهم می‌کند."
        ),
        "location": "تهران، شهرک صنعتی شمس‌آباد",
        "latitude": Decimal("35.345833"),
        "longitude": Decimal("51.153056"),
        "features": ["طراحی اختصاصی", "نصب و راه‌اندازی", "پشتیبانی فنی"],
    },
)


def seed_sample_projects(apps, schema_editor):
    Project = apps.get_model("main", "Project")
    ProjectFeature = apps.get_model("main", "ProjectFeature")

    for project_data in SAMPLE_PROJECTS:
        features = project_data["features"]
        defaults = {
            key: value
            for key, value in project_data.items()
            if key not in {"slug", "features"}
        }
        project, _ = Project.objects.get_or_create(
            slug=project_data["slug"],
            defaults=defaults,
        )
        for position, title in enumerate(features, start=1):
            ProjectFeature.objects.get_or_create(
                project=project,
                title=title,
                defaults={"position": position},
            )


def remove_sample_projects(apps, schema_editor):
    Project = apps.get_model("main", "Project")
    Project.objects.filter(
        slug__in=[project["slug"] for project in SAMPLE_PROJECTS]
    ).delete()


class Migration(migrations.Migration):
    dependencies = [("main", "0005_project_projectgalleryimage_projectfeature_and_more")]

    operations = [
        migrations.RunPython(seed_sample_projects, remove_sample_projects),
    ]
