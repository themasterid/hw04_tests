# deals/tests/tests_form.py
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..forms import PostForm
from ..models import Group, Post

User = get_user_model()

TEXT_POST = 'Текст поста'


class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='Тестовое название группы',
            slug='test_slug',
            description='Тестовое описание группы',
        )
        cls.group_empty = Group.objects.create(
            title='Группа без поста',
            slug='no_post_group',
            description='Группа без поста...',
        )
        cls.form = PostForm()

    def setUp(self):
        self.user = User.objects.create_user(username='post_author')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_post(self):
        """Проверка создания записи в Post."""
        posts_count = Post.objects.count()
        form_data = {
            'text': TEXT_POST,
            'group': self.group.id,
        }
        response = self.authorized_client.post(
            reverse('posts:create'),
            data=form_data,
            follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertRedirects(
            response, reverse(
                'posts:profile',
                kwargs={'username': self.user.username}))
        self.assertEqual(Post.objects.count(), posts_count + 1)
        post_req_index = self.client.get(reverse('posts:index'))
        post_req_group = self.client.get(
            reverse(
                'posts:group_list',
                kwargs={'slug': self.group.slug}))
        post_req_profile = self.client.get(
            reverse(
                'posts:profile',
                kwargs={'username': self.user.username}))

        index_object = post_req_index.context['page_obj'][0]
        self.assertEqual(index_object.text, TEXT_POST)
        self.assertEqual(index_object.author, self.user)
        self.assertEqual(index_object.group, self.group)
        self.assertNotEqual(index_object.group, self.group_empty)

        group_object = post_req_group.context['page_obj'][0]
        self.assertEqual(group_object.text, TEXT_POST)
        self.assertEqual(group_object.author, self.user)
        self.assertEqual(group_object.group, self.group)
        self.assertNotEqual(group_object.group, self.group_empty)

        profile_object = post_req_profile.context['page_obj'][0]
        self.assertEqual(profile_object.text, TEXT_POST)
        self.assertEqual(profile_object.author, self.user)
        self.assertEqual(profile_object.group, self.group)
        self.assertNotEqual(profile_object.group, self.group_empty)

        self.assertTrue(
            Post.objects.filter(
                text=TEXT_POST,
                author=self.user,
                group=self.group,
            ).exists()
        )


class PostEditFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username='post_author',
        )
        cls.group = Group.objects.create(
            title='Тестовое название группы',
            slug='test_slug',
            description='Тестовое описание группы',
        )
        cls.post = Post.objects.create(
            text='Текст поста',
            author=PostEditFormTests.user,
            group=PostEditFormTests.group,
        )
        cls.group_empty = Group.objects.create(
            title='Группа без поста',
            slug='no_post_group',
            description='Группа без поста...',
        )
        cls.form = PostForm()

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_author_edit_post(self):
        """Проверка автор поста редактирует пост."""
        form_data = {
            'text': 'Новый текст поста',
            'group': self.group_empty.id,
        }
        response = self.authorized_client.post(
            reverse(
                'posts:edit',
                args=[self.post.id]),
            data=form_data,
            follow=True
        )
        self.assertRedirects(
            response,
            reverse('posts:post_detail', kwargs={'post_id': self.post.id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        post_request = self.authorized_client.get(reverse('posts:index'))
        first_object = post_request.context.get('page_obj').object_list[0]
        self.assertEqual(first_object.text, 'Новый текст поста')
        self.assertEqual(first_object.author, self.user)
        self.assertEqual(first_object.group, self.group_empty)
        self.assertTrue(
            Post.objects.filter(
                text='Новый текст поста',
                author=self.user,
                group=self.group_empty,
            ).exists()
        )
        self.assertEqual(
            Post.objects.filter(group=self.group).count(), 0)
