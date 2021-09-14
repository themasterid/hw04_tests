from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse


class StaticViewsTests(TestCase):
    def setUp(self):
        self.user_guest = Client()

    def test_about_page_name(self):
        name_status = {
            reverse('about:author'): HTTPStatus.OK,
            reverse('about:tech'): HTTPStatus.OK,
        }
        for name, status in name_status.items():
            with self.subTest(name=name):
                status_code_ = self.user_guest.get(name).status_code
                self.assertEqual(status_code_, status)

    def test_about_page_template(self):
        name_template = {
            reverse('about:author'): 'about/author.html',
            reverse('about:tech'): 'about/tech.html',
        }
        for reverse_name, template in name_template.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.user_guest.get(reverse_name)
                self.assertTemplateUsed(response, template)
