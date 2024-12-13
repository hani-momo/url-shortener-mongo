from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

from ..models import URL

from mongoengine import connect, disconnect
import mongomock


class MongoTestCase(APITestCase):
    def setUp(self):
        connect('shorturl_db', 'mongo://localhost', mongo_client_class=mongomock.MongoClient)
        print("Connected to mock MongoDB")

    def tearDown(self):
        disconnect()

class ShortenURLViewTest(MongoTestCase):

    def test_generated_short_url_length(self):
        original_url = 'http://example.com'
        URL.objects.create(original_url=original_url, shortened_url='abc123')

        response = self.client.post(reverse('api:shorten_url'), {'url': original_url})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data['shortened_url']), 6)


class RedirectViewTestCase(MongoTestCase):

    def test_redirect_with_invalid_short_url_input(self):
        '''Test RedirectView request with invalid short url length'''
        invalid_short_urls = [
            'aabbcc112233',
            'a',
            'a!@#',
        ]
        for invalid_short_url in invalid_short_urls:
            with self.subTest(invalid_short_url=invalid_short_url):
                response = self.client.get(reverse('api:redirect_url', args=[invalid_short_url]))
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_redirect_with_empty_short_url_input(self):
        '''Test RedirectView request with invalid empty short url'''
        empty_short_url = ''
        response = self.client.get(reverse('api:redirect_url', kwargs={'short_url': empty_short_url}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
