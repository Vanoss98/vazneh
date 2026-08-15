from django.db import migrations


SAMPLE_DETAILS = {
    "جرثقیل-سقفی-تک-پل-نمونه": (
        "این محصول با توجه به ابعاد سالن، ظرفیت مورد نیاز و شرایط کاری پروژه "
        "طراحی می‌شود. سازه کم‌حجم، دسترسی آسان برای تعمیرات و امکان انتخاب "
        "تجهیزات کنترلی متنوع، آن را به گزینه‌ای اقتصادی برای خطوط تولید و "
        "انبارهای صنعتی تبدیل می‌کند."
    ),
    "جرثقیل-سقفی-دو-پل-نمونه": (
        "مدل دو پل برای چرخه‌های کاری سنگین، ظرفیت‌های بالا و دهانه‌های بزرگ "
        "مناسب است. طراحی و ساخت هر دستگاه بر اساس استانداردهای صنعتی انجام "
        "می‌شود و امکان افزودن کابین، کنترل از راه دور و تجهیزات ایمنی اختصاصی "
        "وجود دارد."
    ),
}


def populate_sample_details(apps, schema_editor):
    Product = apps.get_model("main", "Product")
    for slug, description in SAMPLE_DETAILS.items():
        Product.objects.filter(slug=slug).update(detailed_description=description)


def clear_sample_details(apps, schema_editor):
    Product = apps.get_model("main", "Product")
    Product.objects.filter(slug__in=SAMPLE_DETAILS).update(detailed_description="")


class Migration(migrations.Migration):
    dependencies = [("main", "0003_product_detailed_description")]

    operations = [
        migrations.RunPython(populate_sample_details, clear_sample_details),
    ]
