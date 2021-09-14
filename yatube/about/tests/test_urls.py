from http import HTTPStatus

from django.test import Client, TestCase


class StaticURLTests(TestCase):
    def setUp(self):
        self.user_guest = Client()

    def test_about_url_exists_at_desired_location(self):
        """Проверка адреса about."""
        url_code = {
            '/about/author/': HTTPStatus.OK,
            '/about/tech/': HTTPStatus.OK,
        }
        for url, code in url_code.items():
            with self.subTest(url=url):
                status = self.user_guest.get(url).status_code
                self.assertEqual(status, code)

    def test_about_url_uses_correct_template(self):
        """Проверка шаблона about."""
        url_templates = {
            '/about/author/': 'about/author.html',
            '/about/tech/': 'about/tech.html',
        }
        for url, template in url_templates.items():
            with self.subTest(url=url):
                adress_url = self.user_guest.get(url)
                self.assertTemplateUsed(adress_url, template)
