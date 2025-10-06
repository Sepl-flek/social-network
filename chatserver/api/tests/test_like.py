from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from chat.models import Post

User = get_user_model()


class LikeAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.post = Post.objects.create(owner=self.user, text='test')

        token = AccessToken.for_user(self.user)

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_like(self):
        url = f"/api/posts/{self.post.pk}/like/"
        response = self.client.post(url)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertTrue(self.post.likes.filter(id=self.user.id).exists())

        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertFalse(self.post.likes.filter(id=self.user.id).exists())
