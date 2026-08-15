import importlib

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
