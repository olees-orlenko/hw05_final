from http import HTTPStatus

from django.core.cache import cache
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post, User
from posts.tests.constants import (
    GROUP_DESCRIPTION,
    GROUP_LIST_REVERSE,
    GROUP_LIST_TEMPLATE,
    GROUP_SLUG,
    GROUP_TITLE,
    INDEX_REVERSE,
    INDEX_TEMPLATE,
    POST_CREATE_REVERSE,
    POST_CREATE_TEMPLATE,
    POST_DETAIL_TEMPLATE,
    POST_DETAIL_URL_NAME,
    POST_EDIT_TEMPLATE,
    POST_EDIT_URL_NAME,
    POST_TEXT,
    PROFILE_REVERSE,
    PROFILE_TEMPLATE,
    URL_UNEXISTING_PAGE,
    USER_USERNAME,
)


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username=USER_USERNAME)
        cls.group = Group.objects.create(
            title=GROUP_TITLE,
            slug=GROUP_SLUG,
            description=GROUP_DESCRIPTION,
        )
        cls.post = Post.objects.create(
            author=cls.author,
            group=cls.group,
            text=POST_TEXT,
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.author)
        cache.clear()

    def test_url_exists_at_desired_location(self):
        """Проверка доступности адресов."""
        pages_url = {
            INDEX_REVERSE: HTTPStatus.OK,
            GROUP_LIST_REVERSE: HTTPStatus.OK,
            PROFILE_REVERSE: HTTPStatus.OK,
            reverse(
                POST_DETAIL_URL_NAME,
                kwargs={'post_id': self.post.id}
            ): HTTPStatus.OK,
            URL_UNEXISTING_PAGE: HTTPStatus.NOT_FOUND,
        }
        for address, http_status in pages_url.items():
            with self.subTest(address=address):
                response = Client().get(address)
                self.assertEqual(response.status_code, http_status)

    def test_post_edit_url_exists_at_desired_location(self):
        """Проверка доступности адреса /posts/1/edit/."""
        response = self.authorized_client.get(
            reverse(
                POST_EDIT_URL_NAME,
                kwargs={'post_id': self.post.id}
            )
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_create_post_url_exists_at_desired_location(self):
        """Проверка доступности адреса /create/."""
        response = self.authorized_client.get(POST_CREATE_REVERSE)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_uses_correct_template(self):
        """Проверка шаблона для адресов."""
        templates_url_names = {
            INDEX_REVERSE: INDEX_TEMPLATE,
            GROUP_LIST_REVERSE: GROUP_LIST_TEMPLATE,
            PROFILE_REVERSE: PROFILE_TEMPLATE,
            reverse(POST_DETAIL_URL_NAME, kwargs={'post_id': self.post.id}):
            POST_DETAIL_TEMPLATE,
            reverse(POST_EDIT_URL_NAME, kwargs={'post_id': self.post.id}):
            POST_EDIT_TEMPLATE,
            POST_CREATE_REVERSE: POST_CREATE_TEMPLATE,
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)
