import importlib
import importlib.util
import os
import subprocess
import sys
from types import SimpleNamespace

from django.apps import apps
from django.conf import settings
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase, TestCase
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
                "DJANGO_ALLOWED_HOSTS": "localhost,127.0.0.1,.vercel.app",
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
                    "print(settings.SECURE_PROXY_SSL_HEADER); "
                    "print(getattr(settings, 'STORAGES', {}).get('default', {}).get('BACKEND', ''))"
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
                "True",
                "['localhost', '127.0.0.1', '.vercel.app', 'vaznehco.com', 'www.vaznehco.com']",
                "['https://vaznehco.com', 'https://www.vaznehco.com', 'https://vazneh-example.vercel.app']",
                "True",
                "True",
                "('HTTP_X_FORWARDED_PROTO', 'https')",
                "main.storage.VercelBlobStorage",
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


class VercelBlobStorageTests(SimpleTestCase):
    def storage_class(self):
        if importlib.util.find_spec("main.storage") is None:
            self.fail("main.storage does not exist")
        storage_module = importlib.import_module("main.storage")
        storage_class = getattr(storage_module, "VercelBlobStorage", None)
        self.assertIsNotNone(storage_class)
        return storage_class

    def test_uploads_to_public_blob_and_returns_its_url(self):
        blob_url = (
            "https://example.public.blob.vercel-storage.com/"
            "projects/main/crane-random.png"
        )

        class BlobClient:
            def put(self, *args, **kwargs):
                self.args = args
                self.kwargs = kwargs
                return SimpleNamespace(url=blob_url)

        client = BlobClient()
        storage = self.storage_class()(client=client)

        saved_name = storage.save(
            "projects/main/crane.png",
            ContentFile(b"image bytes"),
        )

        self.assertEqual(saved_name, blob_url)
        self.assertEqual(storage.url(saved_name), blob_url)
        self.assertEqual(client.args, ("projects/main/crane.png", b"image bytes"))
        self.assertEqual(client.kwargs["access"], "public")
        self.assertTrue(client.kwargs["add_random_suffix"])

    def test_project_image_field_accepts_a_complete_blob_url(self):
        self.assertGreaterEqual(
            Project._meta.get_field("main_image").max_length,
            500,
        )

    def test_opens_blob_content_for_django_file_fields(self):
        class BlobClient:
            def get(self, name):
                self.name = name
                return SimpleNamespace(content=b"stored image")

        client = BlobClient()
        storage = self.storage_class()(client=client)

        stored_file = storage.open(
            "https://example.public.blob.vercel-storage.com/crane.png"
        )

        self.assertEqual(stored_file.read(), b"stored image")
        self.assertEqual(
            client.name,
            "https://example.public.blob.vercel-storage.com/crane.png",
        )


class CatalogDownloadTests(TestCase):
    def catalog_model(self):
        catalog_model = apps.all_models["main"].get("catalog")
        self.assertIsNotNone(catalog_model)
        return catalog_model

    def test_latest_catalog_is_linked_from_all_catalog_download_buttons(self):
        Catalog = self.catalog_model()
        catalog = Catalog.objects.create(file="catalogs/vazneh.pdf")
        product = Product.objects.filter(is_active=True).first()
        service = Service.objects.filter(is_active=True).first()

        for url in (
            "/",
            "/about/",
            product.get_absolute_url(),
            service.get_absolute_url(),
        ):
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertContains(response, f'href="{catalog.file.url}"')

    def test_catalog_only_accepts_pdf_files(self):
        Catalog = self.catalog_model()
        catalog = Catalog(
            file=SimpleUploadedFile("catalog.txt", b"not a pdf"),
        )

        with self.assertRaises(ValidationError):
            catalog.full_clean()

    def test_catalog_can_be_managed_in_django_admin(self):
        Catalog = self.catalog_model()

        self.assertTrue(admin.site.is_registered(Catalog))


class CatalogueContentTests(TestCase):
    def test_contact_page_embeds_the_confirmed_google_map(self):
        response = self.client.get("/contact/")

        self.assertContains(
            response,
            "https://www.google.com/maps/embed?pb=!1m14!1m8!1m3!1d404.8482932690663",
        )

    def test_contact_page_does_not_show_the_company_website(self):
        response = self.client.get("/contact/")

        self.assertNotContains(response, "www.vaznehco.com")

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

    def test_about_page_uses_contact_image_without_slider_controls(self):
        response = self.client.get("/about/")

        self.assertContains(response, 'src="/static/contact-header.jpeg"')
        self.assertNotContains(response, 'id="hero-previous"')
        self.assertNotContains(response, 'id="hero-next"')

    def test_placeholder_certificates_and_home_video_are_hidden(self):
        about_response = self.client.get("/about/")
        home_response = self.client.get("/")

        self.assertNotContains(about_response, "گواهینامه‌های وزنه")
        self.assertNotContains(home_response, "وزنه چطور کار می‌کند؟")

    def test_home_page_does_not_show_fabricated_testimonials(self):
        response = self.client.get("/")

        self.assertNotContains(response, "مشتری اول")
        self.assertNotContains(response, "مدیر پروژه صنایع آریا")
