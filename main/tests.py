import importlib
import os
import subprocess
import sys

from django.conf import settings
from django.test import TestCase
from django.test.utils import override_settings
from django.urls import clear_url_caches


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
    def test_vercel_postgres_url_is_used_when_database_url_is_missing(self):
        environment = os.environ.copy()
        environment.pop("DATABASE_URL", None)
        environment.update(
            {
                "DJANGO_SECRET_KEY": "deployment-secret",
                "POSTGRES_URL": "postgresql://user:password@db.example.com/vazneh",
                "VERCEL": "1",
            }
        )

        result = subprocess.run(
            [
                sys.executable,
                "-c",
                (
                    "from vazneh import settings; "
                    "print(settings.DATABASES['default']['ENGINE']); "
                    "print(settings.DATABASES['default']['NAME'])"
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
            ["django.db.backends.postgresql", "vazneh"],
        )

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
