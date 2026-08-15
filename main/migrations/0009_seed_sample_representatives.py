from decimal import Decimal

from django.db import migrations


REPRESENTATIVES = (
    {
        "name": "مهندس علی رضایی",
        "city": "تهران",
        "phone": "+98 912 100 1100",
        "address": "تهران، خیابان وزرا، ساختمان ساموت، طبقه دوم",
        "latitude": Decimal("35.721900"),
        "longitude": Decimal("51.334700"),
    },
    {
        "name": "مهندس مهدی کاظمی",
        "city": "اصفهان",
        "phone": "+98 913 565 6565",
        "address": "اصفهان، خیابان چهارباغ بالا، مجتمع اداری سپهر",
        "latitude": Decimal("32.654600"),
        "longitude": Decimal("51.668000"),
    },
    {
        "name": "مهندس سارا احمدی",
        "city": "شیراز",
        "phone": "+98 917 220 3300",
        "address": "شیراز، بلوار چمران، ساختمان پارس",
        "latitude": Decimal("29.591800"),
        "longitude": Decimal("52.583700"),
    },
    {
        "name": "مهندس امیر موسوی",
        "city": "رشت",
        "phone": "+98 911 340 4500",
        "address": "رشت، بلوار گیلان، مجتمع تجاری گلسار",
        "latitude": Decimal("37.280800"),
        "longitude": Decimal("49.583200"),
    },
    {
        "name": "مهندس رضا اکبری",
        "city": "تبریز",
        "phone": "+98 914 670 7800",
        "address": "تبریز، ولیعصر، خیابان شهریار",
        "latitude": Decimal("38.080000"),
        "longitude": Decimal("46.291900"),
    },
    {
        "name": "مهندس نازنین کریمی",
        "city": "کرمان",
        "phone": "+98 913 880 9900",
        "address": "کرمان، بلوار جمهوری اسلامی، برج تجاری باران",
        "latitude": Decimal("30.283900"),
        "longitude": Decimal("57.083400"),
    },
)


def seed_representatives(apps, schema_editor):
    Representative = apps.get_model("main", "Representative")
    for representative in REPRESENTATIVES:
        Representative.objects.get_or_create(
            city=representative["city"],
            phone=representative["phone"],
            defaults=representative,
        )


def remove_representatives(apps, schema_editor):
    Representative = apps.get_model("main", "Representative")
    Representative.objects.filter(
        phone__in=[representative["phone"] for representative in REPRESENTATIVES]
    ).delete()


class Migration(migrations.Migration):
    dependencies = [("main", "0008_representative")]

    operations = [
        migrations.RunPython(seed_representatives, remove_representatives),
    ]
