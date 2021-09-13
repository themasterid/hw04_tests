# posts/tests/tests_url.py
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from ..models import Group, Post

User = get_user_model()

INDEX_URL = '/'
GROUP_URL = 'group'
PROFILE_URL = 'profile'
SLUG_URL = 'real_slug'
BAD_SLUG_URL = 'bad_slug'
USER_AUTHOR_URL = 'user_author'
ANOTHER_USER_URL = 'another_user'
POSTS_URL = 'posts'
EDIT_URL = 'edit'
POST_N_URL = '1'
CREATE_URL = 'create'
NOT_FOUND = 'unexisting_page'

ABOUT_URL = 'about'
AUTH_URL = 'auth'


class StaticURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='Тестовое название группы',
            slug=f'{SLUG_URL}',
            description='Тестовое описание группы',
        )
        cls.user_author = User.objects.create_user(
            username=f'{USER_AUTHOR_URL}')
        cls.another_user = User.objects.create_user(
            username=f'{ANOTHER_USER_URL}')
        cls.post = Post.objects.create(
            text='Текст который просто больше 15 символов...',
            author=StaticURLTests.user_author,
            group=StaticURLTests.group,
        )

    def setUp(self):
        self.unauthorized_user = Client()
        self.post_author = Client()
        self.post_author.force_login(self.user_author)
        self.authorized_user = Client()
        self.authorized_user.force_login(self.another_user)

    def test_all_static_pages(self):
        """Проверка статичных страниц для неавторизованного пользователя."""
        field_urls_code = {
            INDEX_URL: HTTPStatus.OK,
            f'/{ABOUT_URL}/author/': HTTPStatus.OK,
            f'/{ABOUT_URL}/tech/': HTTPStatus.OK,
            f'/{NOT_FOUND}/': HTTPStatus.NOT_FOUND,
            f'/{AUTH_URL}/signup/': HTTPStatus.OK,
            f'/{AUTH_URL}/logout/': HTTPStatus.OK,
            f'/{AUTH_URL}/login/': HTTPStatus.OK,
            f'/{AUTH_URL}/password_change/': HTTPStatus.FOUND,
            f'/{AUTH_URL}/password_change/done/': HTTPStatus.FOUND,
            f'/{AUTH_URL}/password_reset/': HTTPStatus.OK,
            f'/{AUTH_URL}/password_reset/done/': HTTPStatus.OK,
            f'/{AUTH_URL}/reset/done/': HTTPStatus.OK,
        }
        for url, response_code in field_urls_code.items():
            with self.subTest(url=url):
                status_code = self.unauthorized_user.get(url).status_code
                self.assertEqual(status_code, response_code)

    def test_unauthorized_user_urls_status_code(self):
        """Проверка status_code для неавторизованного пользователя."""
        field_urls_code = {
            INDEX_URL: HTTPStatus.OK,
            f'/{GROUP_URL}/{SLUG_URL}/': HTTPStatus.OK,
            f'/{GROUP_URL}/{BAD_SLUG_URL}/': HTTPStatus.NOT_FOUND,
            f'/{PROFILE_URL}/{USER_AUTHOR_URL}/': HTTPStatus.OK,
            f'/{POSTS_URL}/{POST_N_URL}/': HTTPStatus.OK,
            f'/{POSTS_URL}/{POST_N_URL}/{EDIT_URL}/': HTTPStatus.FOUND,
            f'/{CREATE_URL}/': HTTPStatus.FOUND,
            f'/{NOT_FOUND}/': HTTPStatus.NOT_FOUND,
        }
        for url, response_code in field_urls_code.items():
            with self.subTest(url=url):
                status_code = self.unauthorized_user.get(url).status_code
                self.assertEqual(status_code, response_code)

    def test_authorized_user_urls_status_code(self):
        """Проверка status_code для авторизованного пользователя."""
        field_urls_code = {
            INDEX_URL: HTTPStatus.OK,
            f'/{GROUP_URL}/{SLUG_URL}/': HTTPStatus.OK,
            f'/{GROUP_URL}/{BAD_SLUG_URL}/': HTTPStatus.NOT_FOUND,
            f'/{PROFILE_URL}/{USER_AUTHOR_URL}/': HTTPStatus.OK,
            f'/{POSTS_URL}/{POST_N_URL}/': HTTPStatus.OK,
            f'/{POSTS_URL}/{POST_N_URL}/{EDIT_URL}/': HTTPStatus.FOUND,
            f'/{CREATE_URL}/': HTTPStatus.OK,
            f'/{NOT_FOUND}/': HTTPStatus.NOT_FOUND,
        }
        for url, response_code in field_urls_code.items():
            with self.subTest(url=url):
                status_code = self.authorized_user.get(url).status_code
                self.assertEqual(status_code, response_code)

    def test_author_user_urls_status_code(self):
        """Проверка status_code для автора постов."""
        field_urls_code = {
            INDEX_URL: HTTPStatus.OK,
            f'/{GROUP_URL}/{SLUG_URL}/': HTTPStatus.OK,
            f'/{GROUP_URL}/{BAD_SLUG_URL}/': HTTPStatus.NOT_FOUND,
            f'/{PROFILE_URL}/{USER_AUTHOR_URL}/': HTTPStatus.OK,
            f'/{POSTS_URL}/{POST_N_URL}/': HTTPStatus.OK,
            f'/{POSTS_URL}/{POST_N_URL}/{EDIT_URL}/': HTTPStatus.OK,
            f'/{CREATE_URL}/': HTTPStatus.OK,
            f'/{NOT_FOUND}/': HTTPStatus.NOT_FOUND,
        }
        for url, response_code in field_urls_code.items():
            with self.subTest(url=url):
                status_code = self.post_author.get(url).status_code
                self.assertEqual(status_code, response_code)

    def test_urls_template(self):
        """Проверка urls и template для авторизованного пользователя."""
        templates_url_names = {
            INDEX_URL: 'posts/index.html',
            f'/{GROUP_URL}/{SLUG_URL}/': 'posts/group_list.html',
            f'/{PROFILE_URL}/{USER_AUTHOR_URL}/': 'posts/profile.html',
            f'/{POSTS_URL}/{POST_N_URL}/': 'posts/post_detail.html',
            f'/{CREATE_URL}/': 'posts/create_post.html',
            f'/{POSTS_URL}/{POST_N_URL}/{EDIT_URL}/': 'posts/create_post.html',
        }
        for adress, template in templates_url_names.items():
            with self.subTest(adress=adress):
                adress_url = self.post_author.get(adress)
                self.assertTemplateUsed(adress_url, template)
