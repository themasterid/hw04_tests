# posts/tests/test_views.py
from django import forms
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post

User = get_user_model()


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание группы',
        )
        cls.post = Post.objects.create(
            text='Тестовый текст поста',
            author=cls.user,
            group=cls.group,
        )
        cls.group_none = Group.objects.create(
            title='None группа',
            slug='bad-slug',
            description='Описание None группы',
        )

    def setUp(self):
        self.user = PostPagesTests.user
        self.post = PostPagesTests.post
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        """Проверка URL-адреса используют соответствующий шаблон."""
        templates_pages_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse(
                'posts:group_list',
                kwargs={'slug': self.group.slug}): 'posts/group_list.html',
            reverse(
                'posts:profile',
                kwargs={'username': self.user.username}): 'posts/profile.html',
            reverse(
                'posts:post_detail',
                kwargs={'post_id': self.post.id}): 'posts/post_detail.html',
            reverse(
                'posts:edit',
                kwargs={'post_id': self.post.id}): 'posts/create_post.html',
            reverse('posts:create'): 'posts/create_post.html',
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_page_show_correct_context(self):
        """Шаблон index.html сформирован с правильным контекстом."""
        context = {
            reverse('posts:index'): self.post,
            reverse(
                'posts:group_list',
                kwargs={'slug': self.group.slug, }): self.post,
            reverse(
                'posts:profile',
                kwargs={'username': self.user.username, }): self.post,
        }
        for reverse_page, object in context.items():
            with self.subTest(reverse_page=reverse_page):
                response = self.authorized_client.get(reverse_page)
                page_object = response.context['page_obj'][0]
                self.assertEqual(page_object.text, object.text)
                self.assertEqual(page_object.pub_date, object.pub_date)
                self.assertEqual(page_object.author, object.author)
                self.assertEqual(page_object.group, object.group)

    def test_groups_page_show_correct_context(self):
        """Шаблон group_list.html сформирован с правильным контекстом."""
        context = {
            reverse(
                'posts:group_list',
                kwargs={'slug': self.group.slug}): self.group,
            reverse(
                'posts:group_list',
                kwargs={'slug': self.group_none.slug}): self.group_none,
        }
        response = self.authorized_client.get(
            reverse('posts:group_list',
                    kwargs={'slug': self.group_none.slug}))
        self.assertFalse(response.context['page_obj'])
        for reverse_page, object in context.items():
            with self.subTest(reverse_page=reverse_page):
                response = self.authorized_client.get(reverse_page)
                group_object = response.context['group']
                self.assertEqual(group_object.title, object.title)
                self.assertEqual(group_object.slug, object.slug)
                self.assertEqual(
                    group_object.description,
                    object.description)

    def test_profile_page_show_correct_context(self):
        """Шаблон profile.html сформирован с правильным контекстом."""
        # ! не закончен
        context = {
            reverse(
                'posts:profile',
                kwargs={'username': self.user.username}): self.user,
        }
        for reverse_page, object in context.items():
            with self.subTest(reverse_page=reverse_page):
                response = self.authorized_client.get(reverse_page)
                author_object = response.context['author']
                self.assertEqual(author_object.id, object.id)
                self.assertEqual(author_object.username, object.username)

    def test_detail_page_show_correct_context(self):
        """Шаблон post_detail.html сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:post_detail',
                    kwargs={'post_id': self.post.id}))
        post_object = response.context['post']
        self.assertEqual(post_object.text, self.post.text)
        self.assertEqual(post_object.pub_date, self.post.pub_date)
        self.assertEqual(post_object.author, self.user)
        self.assertEqual(post_object.group, self.group)

    def test_forms_show_correct(self):
        """Проверка коректности формы."""
        context = {
            reverse('posts:create'),
            reverse('posts:edit',
                    kwargs={'post_id': self.post.id,
                            }),
        }
        for reverse_page in context:
            with self.subTest(reverse_page=reverse_page):
                response = self.authorized_client.get(reverse_page)
                self.assertIsInstance(
                    response.context['form'].fields['text'],
                    forms.fields.CharField)
                self.assertIsInstance(
                    response.context['form'].fields['group'],
                    forms.fields.ChoiceField)


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(
            username='posts_author',
        )
        cls.group = Group.objects.create(
            title='Тестовое название группы',
            slug='test-slug',
            description='Тестовое описание группы',
        )
        cls.post = [
            Post.objects.create(
                text='Пост №' + str(i),
                author=PaginatorViewsTest.user,
                group=PaginatorViewsTest.group
            )
            for i in range(13)]

    def setUp(self):
        self.auth_user = User.objects.create(
            username='auth'
        )
        self.user_client = Client()
        self.user_client.force_login(self.auth_user)
        self.user_client.get(
            reverse(
                'posts:profile',
                kwargs={'username': self.user.username}))

    def test_paginator_on_pages(self):
        """Проверка пагинации на страницах."""
        first_page_len_posts = 10
        second_page_len_posts = 3
        context = {
            reverse('posts:index'): first_page_len_posts,
            reverse('posts:index') + '?page=2': second_page_len_posts,
            reverse('posts:group_list', kwargs={'slug': self.group.slug, }):
            first_page_len_posts,
            reverse('posts:group_list', kwargs={'slug': self.group.slug, })
            + '?page=2': second_page_len_posts,
            reverse('posts:profile', kwargs={'username': self.user.username}):
            first_page_len_posts,
            reverse('posts:profile', kwargs={'username': self.user.username})
            + '?page=2': second_page_len_posts,
        }
        for reverse_page, len_posts in context.items():
            with self.subTest(reverse=reverse):
                self.assertEqual(len(self.user_client.get(
                    reverse_page).context.get('page_obj')), len_posts)

    def test_object_list_first_page(self):
        """Проверка пагинации на первой странице."""
        response = self.client.get(reverse('posts:index'))
        for i in range(10):
            page_object = response.context.get('page_obj').object_list[i]
            expected_object = response.context['page_obj'][i]
            self.assertEqual(page_object.author, expected_object.author)
            self.assertEqual(page_object.text, expected_object.text)
            self.assertEqual(page_object.group, expected_object.group)
            self.assertEqual(
                page_object.pub_date,
                expected_object.pub_date)

    def test_object_list_second_page(self):
        """Проверка пагинации на следующей странице."""
        response = self.client.get(reverse('posts:index') + '?page=2')
        for i in range(3):
            page_object = response.context.get('page_obj').object_list[i]
            expected_object = response.context['page_obj'][i]
            self.assertEqual(page_object.author, expected_object.author)
            self.assertEqual(page_object.text, expected_object.text)
            self.assertEqual(page_object.group, expected_object.group)
            self.assertEqual(
                page_object.pub_date,
                expected_object.pub_date)
