from http import HTTPStatus

import shutil
import tempfile

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from posts.models import Group, Post, User
from posts.tests.constants import (
    AUTHOR_USERNAME,
    GROUP_DESCRIPTION,
    GROUP_SLUG,
    GROUP_SLUG_1,
    GROUP_TITLE,
    IMAGE,
    IMAGE_ROOT,
    SMALL_GIF,
    POST_CREATE_REVERSE,
    POST_DETAIL_URL_NAME,
    PROFILE_URL_NAME,
    POST_EDIT_URL_NAME,
    POST_EDIT_TEXT,
    POST_TEXT,
    USER_USERNAME,
)

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username=AUTHOR_USERNAME)
        cls.user = User.objects.create_user(username=USER_USERNAME)
        cls.group = Group.objects.create(
            title=GROUP_TITLE,
            slug=GROUP_SLUG,
            description=GROUP_DESCRIPTION,
        )
        cls.form_data_edit = {'text': POST_EDIT_TEXT, 'group': cls.group.id}
        cls.uploaded = SimpleUploadedFile(
            name=IMAGE,
            content=SMALL_GIF,
            content_type='image/gif',
        )
        cls.form_data = {
            'text': POST_TEXT,
            'group': cls.group.id,
            'image': cls.uploaded
        }
        cls.post = Post.objects.create(
            author=cls.author,
            group=cls.group,
            text=POST_TEXT,
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.author)

    def test_create_post(self):
        """При отправке валидной формы создаётся новая запись."""
        post_latest = Post.objects.latest('id')
        posts_count = Post.objects.count()
        self.form_data = {
            'text': POST_TEXT,
            'image': self.uploaded
        }
        response = self.authorized_client.post(
            POST_CREATE_REVERSE, data=self.form_data, follow=True
        )
        self.assertRedirects(
            response, reverse(
                PROFILE_URL_NAME,
                kwargs={'username': self.post.author}
            )
        )
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertEqual(post_latest.text, self.form_data['text'])
        self.assertTrue(
            Post.objects.filter(
                group=self.group, author=self.author
            ).exists()
        )
        self.assertTrue(
            Post.objects.filter(
                image=IMAGE_ROOT + IMAGE
            ).exists()
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_edit(self):
        """При отправке валидной формы редактирования изменяется пост."""
        posts_count = Post.objects.count()
        response = self.authorized_client.post(
            reverse(POST_EDIT_URL_NAME, kwargs={'post_id': self.post.id}),
            data=self.form_data_edit,
            follow=True,
        )
        self.assertRedirects(
            response, reverse(POST_DETAIL_URL_NAME,
                              kwargs={'post_id': self.post.id})
        )
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertTrue(Post.objects.filter(text=POST_EDIT_TEXT).exists())
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_edit_create_guest_client(self):
        """Валидная форма не изменит запись в Post если неавторизован."""
        self.post = Post.objects.create(
            author=self.user,
            text=POST_TEXT,
        )
        self.group = Group.objects.create(
            title=GROUP_TITLE,
            slug=GROUP_SLUG_1,
            description=GROUP_DESCRIPTION,
        )
        posts_count = Post.objects.count()
        form_data = {'text': POST_EDIT_TEXT, 'group': self.group.id}
        response = self.guest_client.post(
            reverse(POST_EDIT_URL_NAME, kwargs={'post_id': self.post.id}),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(
            response, f'/auth/login/?next=/posts/{self.post.id}/edit/'
        )
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertFalse(Post.objects.filter(text=POST_EDIT_TEXT).exists())
        self.assertEqual(response.status_code, HTTPStatus.OK)
