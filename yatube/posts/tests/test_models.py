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

    def test_post_str(self):
        """Проверка __str__ у post."""
        post = self.post
        self.assertEqual(post.text[:15], str(post))

    def test_post_verbose_name(self):
        """Проверка verbose_name у post."""
        post = self.post
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

    def test_post_help_text(self):
        """Проверка help_text у post."""
        post = self.post
        help_text = post._meta.get_field('text').help_text
        self.assertEqual(help_text, 'Текст нового поста')


class GroupModelTest(TestCase):
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

    def test_group_str(self):
        """Проверка __str__ у group."""
        group = self.group
        self.assertEqual(group.title, str(group))

    def test_group_verbose_name(self):
        """Проверка verbose_name у group."""
        group = self.group
        field_verboses = {
            'title': 'Заголовок',
            'slug': 'ЧПУ',
            'description': 'Описание',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                verbose_name = group._meta.get_field(value).verbose_name
                self.assertEqual(verbose_name, expected)

    def test_group_help_text(self):
        """Проверка help_text у group."""
        post = self.post
        help_text = post._meta.get_field('group').help_text
        self.assertEqual(help_text, 'Группа, к которой будет относиться пост')
