from django.contrib.auth.models import User
from .models import Post
from rest_framework import status
from rest_framework.test import APITestCase


class PostListViewTests(APITestCase):
    def setUp(self):
    # override setUp(), which will be executed automatically before every test method
        User.objects.create_user(username="adam", password="pass")

    def test_can_list_post(self):
        adam = User.objects.get(username="adam")
        Post.objects.create(owner=adam, title="a title")
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))

    def test_logged_in_user_can_create_post(self):
        self.client.login(username="adam", password="pass")
        response = self.client.post("/posts/", {"title":"a title"})
        count = Post.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cannot_create_post_when_logged_out(self):
        response = self.client.post("/posts/", {"title":"a title"})
        count = Post.objects.count()        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class PostDetailTest(APITestCase):
    def setUp(self):
        adam = User.objects.create_user(username="adam", password="pass")
        brian = User.objects.create_user(username="brian", password="pass")
        Post.objects.create(
            owner=adam, title="a title", content="adms content"
        )
        Post.objects.create(
            owner=brian, title="a title", content="brians content"
        )

    def test_can_retrieve_post_using_valid_id(self):
        response = self.client.get('/post/1')
        self.assertEqual(response.data["title"], "a title")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_cannot_retrieve_post_using_invalid_id(self):
        response = self.client.get('/post/5')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_post(self):
        self.client.login(username="adam", password="pass")
        response = self.client.put("/post/1", {"title": "new title", "content": "new content"})
        post = Post.objects.get(pk=1)
        self.assertEqual(post.title, "new title")
        self.assertEqual(post.content, "new content")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_update_someone_elses_post(self):
        self.client.login(username="adam", password="pass")
        response = self.client.put("/post/2", {"title": "new title"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        