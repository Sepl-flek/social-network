from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class FriendsAPITestCase(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create(username='user1', password='1234')
        self.user2 = User.objects.create(username='user2', password='1234')

    def test_friend_request(self):
        url = reverse('customuser-friend-request', args=(self.user2.id,))
        self.client.force_login(self.user1)

        response = self.client.post(url, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertTrue(self.user1 in self.user2.friend_requests.all())

        response = self.client.post(url, content_type='application/json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertTrue(self.user1 in self.user2.friend_requests.all())

        self.client.logout()
        self.client.force_login(self.user2)

        #проверка что добавиться в друзья если будет запрос на добавление в друзья
        another_url = reverse('customuser-friend-request', args=(self.user1.id,))
        response = self.client.post(another_url, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertTrue(self.user1 in self.user2.friends.all())
        self.assertTrue(self.user2 in self.user1.friends.all())
        self.assertFalse(self.user2 in self.user1.friend_requests.all())
        self.assertFalse(self.user1 in self.user2.friend_requests.all())
        self.assertFalse(self.user1 in self.user2.followers.all())
        self.assertFalse(self.user2 in self.user1.followers.all())

        response = self.client.post(url, content_type='application/json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_add_friend(self):
        url_friend = reverse('customuser-friends', args=(self.user2.id,))
        url_friend1 = reverse('customuser-friends', args=(self.user1.id,))
        url_request = reverse('customuser-friend-request', args=(self.user2.id,))
        self.client.force_login(self.user1)
        response = self.client.post(url_friend, content_type='application/json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.client.post(url_request, content_type='application/json')
        self.client.logout()
        self.client.force_login(self.user2)
        response = self.client.post(url_friend1, content_type='application/json')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertTrue(self.user1 in self.user2.friends.all())
        self.assertTrue(self.user2 in self.user1.friends.all())
        self.assertFalse(self.user2 in self.user1.friend_requests.all())
        self.assertFalse(self.user1 in self.user2.friend_requests.all())
        self.assertFalse(self.user1 in self.user2.followers.all())
        self.assertFalse(self.user2 in self.user1.followers.all())

        response = self.client.delete(url_friend1, content_type='application/json')
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertTrue(self.user1 in self.user2.followers.all())
        self.assertFalse(self.user1 in self.user2.friends.all())