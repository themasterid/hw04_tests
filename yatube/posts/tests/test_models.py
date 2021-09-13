from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            text='Тестовый текст больше 15 символов для проверки...',
            author=cls.user,
            group=cls.group,
        )

    def test_str_posts_and_group(self):
        """Проверка __str__ у posts и group."""
        post = self.post
        group = self.group
        filds_str_ = {
            post.text[:15]: str(post)[:15],
            group.title: str(group),
        }
        for value, expected in filds_str_.items():
            self.assertEqual(value, expected)

    def test_post_verbose_name(self):
        """Проверка verbose_name у posts."""
        post = PostModelTest.post
        field_verboses = {
            'text': 'Текст поста',
            'pub_date': 'Дата публикации',
            'author': 'Автор',
            'group': 'Группа',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                verbose_name = post._meta.get_field(value).verbose_name
                self.assertEqual(verbose_name, expected)

    def test_group_verbose_name(self):
        """Проверка verbose_name у group."""
        group = PostModelTest.group
        field_verboses = {
            'title': 'Заголовок',
            'slug': 'ЧПУ',
            'description': 'Описание',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                verbose_name = group._meta.get_field(value).verbose_name
                self.assertEqual(verbose_name, expected)

    def test_post_help_text(self):
        """Проверка help_text у posts."""
        post = PostModelTest.post
        feild_help_texts = {
            'text': 'Введите текст поста',
            'group': 'Выберите группу',
        }
        for value, expected in feild_help_texts.items():
            with self.subTest(value=value):
                help_text = post._meta.get_field(value).help_text
                self.assertEqual(help_text, expected)
