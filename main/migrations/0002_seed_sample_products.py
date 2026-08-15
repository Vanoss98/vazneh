from django.db import migrations


def seed_sample_products(apps, schema_editor):
    Product = apps.get_model("main", "Product")
    ProductCapacity = apps.get_model("main", "ProductCapacity")
    ProductFeature = apps.get_model("main", "ProductFeature")
    ProductSize = apps.get_model("main", "ProductSize")
    ProductType = apps.get_model("main", "ProductType")

    single_girder, _ = ProductType.objects.get_or_create(
        slug="جرثقیل-سقفی-تک-پل",
        defaults={"title": "جرثقیل سقفی تک پل", "position": 1},
    )
    double_girder, _ = ProductType.objects.get_or_create(
        slug="جرثقیل-سقفی-دو-پل",
        defaults={"title": "جرثقیل سقفی دو پل", "position": 2},
    )

    product_one, _ = Product.objects.get_or_create(
        slug="جرثقیل-سقفی-تک-پل-نمونه",
        defaults={
            "product_type": single_girder,
            "title": "جرثقیل سقفی تک پل",
            "subtitle": "راهکاری سبک، اقتصادی و قابل اعتماد",
            "short_description": (
                "جرثقیل سقفی تک پل وزنه برای جابه‌جایی ایمن بار در سالن‌های "
                "صنعتی طراحی شده و متناسب با نیاز پروژه قابل سفارشی‌سازی است."
            ),
            "price": 700000000,
        },
    )
    product_two, _ = Product.objects.get_or_create(
        slug="جرثقیل-سقفی-دو-پل-نمونه",
        defaults={
            "product_type": double_girder,
            "title": "جرثقیل سقفی دو پل",
            "subtitle": "قدرت بیشتر برای پروژه‌های سنگین صنعتی",
            "short_description": (
                "جرثقیل سقفی دو پل وزنه برای ظرفیت‌های بالا و دهانه‌های بزرگ "
                "ساخته می‌شود و امکان افزودن تجهیزات اختصاصی را دارد."
            ),
            "price": 950000000,
        },
    )

    for product, capacities, sizes, features in (
        (
            product_one,
            ["۲ تا ۵ تن", "۵ تا ۱۵ تن"],
            ["سایز ۱", "سایز ۲"],
            ["طراحی کم‌حجم", "نصب سریع", "مصرف انرژی بهینه"],
        ),
        (
            product_two,
            ["۱۰ تا ۳۰ تن", "بیش از ۳۰ تن"],
            ["سایز ۳", "سایز ۴"],
            ["امکان سفارشی‌سازی", "مناسب صنایع سنگین", "کنترل دقیق بار"],
        ),
    ):
        for position, title in enumerate(capacities, start=1):
            ProductCapacity.objects.get_or_create(
                product=product,
                title=title,
                defaults={"position": position},
            )
        for position, title in enumerate(sizes, start=1):
            ProductSize.objects.get_or_create(
                product=product,
                title=title,
                defaults={"position": position},
            )
        for position, title in enumerate(features, start=1):
            ProductFeature.objects.get_or_create(
                product=product,
                title=title,
                defaults={"position": position},
            )

    product_one.similar_products.add(product_two)
    product_two.similar_products.add(product_one)


def remove_sample_products(apps, schema_editor):
    Product = apps.get_model("main", "Product")
    ProductType = apps.get_model("main", "ProductType")

    Product.objects.filter(
        slug__in=(
            "جرثقیل-سقفی-تک-پل-نمونه",
            "جرثقیل-سقفی-دو-پل-نمونه",
        )
    ).delete()
    ProductType.objects.filter(
        slug__in=("جرثقیل-سقفی-تک-پل", "جرثقیل-سقفی-دو-پل"),
        products__isnull=True,
    ).delete()


class Migration(migrations.Migration):
    dependencies = [("main", "0001_initial")]

    operations = [
        migrations.RunPython(seed_sample_products, remove_sample_products),
    ]
