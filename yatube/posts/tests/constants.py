from django.urls import reverse

AUTHOR_USERNAME = 'test_author'
USER_USERNAME = 'test_user'
GROUP_TITLE = 'Тестовая группа'
GROUP_SLUG = 'test-slug'
GROUP_SLUG_1 = 'test'
GROUP_DESCRIPTION = 'Тестовое описание'
POST_TEXT = 'Тестовый пост проверка'
POST_EDIT_TEXT = 'Изменяем пост'
COMMENT_TEXT = 'Тестовый комментарий'

INDEX_URL_NAME = 'posts:index'
GROUP_LIST_URL_NAME = 'posts:group_list'
PROFILE_URL_NAME = 'posts:profile'
POST_DETAIL_URL_NAME = 'posts:post_detail'
POST_EDIT_URL_NAME = 'posts:post_edit'
POST_CREATE_URL_NAME = 'posts:post_create'
POST_DETAIL_COMMENT_URL_NAME = 'posts:add_comment'
POST_FOLLOW_URL_NAME = 'posts:follow_index'

URL_UNEXISTING_PAGE = '/unexisting_page/'
URL_404 = '/nonexist-page/'
INDEX_REVERSE = reverse('posts:index')
POST_CREATE_REVERSE = reverse('posts:post_create')
POST_FOLLOW_REVERSE = reverse('posts:follow_index')
GROUP_LIST_REVERSE = reverse('posts:group_list', kwargs={'slug': GROUP_SLUG})
PROFILE_REVERSE = reverse('posts:profile', kwargs={'username': USER_USERNAME})

INDEX_TEMPLATE = 'posts/index.html'
GROUP_LIST_TEMPLATE = 'posts/group_list.html'
PROFILE_TEMPLATE = 'posts/profile.html'
POST_DETAIL_TEMPLATE = 'posts/post_detail.html'
POST_EDIT_TEMPLATE = 'posts/create_post.html'
POST_CREATE_TEMPLATE = 'posts/create_post.html'
HTTP404_HTML_TEMPLATE = 'core/404.html'
FOLLOW_TEMPLATE = 'posts/follow.html'


IMAGE = 'small.gif'
IMAGE_ROOT = 'posts/'
SMALL_GIF = (
    b'\x47\x49\x46\x38\x39\x61\x01\x00'
    b'\x01\x00\x00\x00\x00\x21\xf9\x04'
    b'\x01\x0a\x00\x01\x00\x2c\x00\x00'
    b'\x00\x00\x01\x00\x01\x00\x00\x02'
    b'\x02\x4c\x01\x00\x3b'
)
