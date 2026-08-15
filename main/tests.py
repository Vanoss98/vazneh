import importlib
import os
import subprocess
import sys

from django.conf import settings
from django.test import TestCase
from django.test.utils import override_settings
from django.urls import clear_url_caches

from .models import BlogPost, Product, Project, Service


class HomePageTests(TestCase):
    def test_home_page_uses_the_index_and_base_templates(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/index.html")
        self.assertTemplateUsed(response, "base.html")
        self.assertContains(
            response,
            "https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4",
        )

    @override_settings(DEBUG=True)
    def test_project_static_files_are_served_in_development(self):
        import vazneh.urls

        clear_url_caches()
        importlib.reload(vazneh.urls)

        response = self.client.get(
            f"{settings.STATIC_URL}logo.svg",
            HTTP_HOST="testserver",
        )

        self.assertEqual(response.status_code, 200)


class ProductionSettingsTests(TestCase):
    def test_vercel_environment_uses_secure_runtime_settings(self):
        environment = os.environ.copy()
        environment.update(
            {
                "DJANGO_SECRET_KEY": "deployment-secret",
                "VERCEL": "1",
                "VERCEL_URL": "vazneh-example.vercel.app",
            }
        )

        result = subprocess.run(
            [
                sys.executable,
                "-c",
                (
                    "from vazneh import settings; "
                    "print(settings.SECRET_KEY); "
                    "print(settings.DEBUG); "
                    "print(settings.ALLOWED_HOSTS); "
                    "print(settings.CSRF_TRUSTED_ORIGINS); "
                    "print(settings.SESSION_COOKIE_SECURE); "
                    "print(settings.CSRF_COOKIE_SECURE); "
                    "print(settings.SECURE_PROXY_SSL_HEADER)"
                ),
            ],
            cwd=settings.BASE_DIR,
            env=environment,
            check=True,
            capture_output=True,
            text=True,
        )

        self.assertEqual(
            result.stdout.splitlines(),
            [
                "deployment-secret",
                "False",
                "['localhost', '127.0.0.1', '.vercel.app']",
                "['https://vazneh-example.vercel.app']",
                "True",
                "True",
                "('HTTP_X_FORWARDED_PROTO', 'https')",
            ],
        )


class EnglishSlugTests(TestCase):
    def test_new_product_slug_uses_english_title(self):
        product = Product.objects.create(
            title="جرثقیل نمونه",
            title_en="Sample Overhead Crane",
            subtitle="نمونه",
            short_description="نمونه",
            price=1,
        )

        self.assertEqual(product.slug, "sample-overhead-crane")

    def test_new_project_slug_uses_english_title(self):
        project = Project.objects.create(
            title="پروژه نمونه",
            title_en="Sample Industrial Project",
            subtitle="نمونه",
            description="نمونه",
            location="تهران",
            latitude=35.6892,
            longitude=51.3890,
        )

        self.assertEqual(project.slug, "sample-industrial-project")


class CatalogueContentTests(TestCase):
    def test_catalogue_products_replace_sample_products(self):
        self.assertEqual(Product.objects.filter(is_active=True).count(), 19)
        self.assertTrue(
            Product.objects.filter(
                slug="single-girder-overhead-crane",
                title="جرثقیل سقفی تک پل",
            ).exists()
        )
        self.assertTrue(
            Product.objects.filter(
                slug="c-hook",
                title="سی هوک",
            ).exists()
        )

    def test_only_catalogue_backed_services_are_active(self):
        self.assertEqual(
            set(Service.objects.filter(is_active=True).values_list("slug", flat=True)),
            {"maintenance", "industrial-structures", "spare-parts"},
        )

    def test_sample_blog_posts_are_unpublished(self):
        self.assertFalse(BlogPost.objects.filter(is_published=True).exists())

    def test_title_only_catalogue_project_renders_without_map_coordinates(self):
        Project.objects.all().delete()
        project = Project.objects.create(
            title="نیروگاه شهید رجایی",
            slug="shahid-rajaei-power-plant",
        )

        response = self.client.get("/projects/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, project.title)
        self.assertEqual(response.context["map_projects"], [])

    def test_about_page_uses_catalogue_company_history(self):
        response = self.client.get("/about/")

        self.assertContains(response, "شرکت وزنه در سال ۱۳۴۳ تأسیس شد")
        self.assertContains(response, "از سال ۱۳۸۵ شرکت وزنه به مجموعه گروه صنعتی ماموت پیوست")

    def test_home_page_does_not_show_fabricated_testimonials(self):
        response = self.client.get("/")

        self.assertNotContains(response, "مشتری اول")
        self.assertNotContains(response, "مدیر پروژه صنایع آریا")
