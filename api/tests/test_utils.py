from unittest.mock import patch
from django.test import TestCase
from rest_framework import status
from django.urls import reverse

from api.models import URL
from api.utils import create_short_url

import mongoengine
import mongomock


mongoengine.connection.disconnect()

@patch('mongoengine.connection.MongoClient', new=mongomock.MongoClient)
class ShortenURLViewTest(TestCase):

    def setUp(self):
        mongoengine.connect('testdb', mongo_client_class=mongomock.MongoClient)
        URL.drop_collection()

    def _fixture_teardown(self):
        pass


    def test_generated_short_url_length(self):
        result1 = create_short_url('AAAAAAAAAA', 6)
        self.assertEqual(len(result1), 6)

        result2 = create_short_url('BBBBBBBBBB', 6)
        self.assertEqual(len(result2), 6)
        self.assertNotEqual(result2, result1)

    def test_try_create_duplicate_original_url(self):
        original_url = "https://github.com"
        short_url = create_short_url(original_url, 6)
        duplicate_short_url = create_short_url(original_url, 6)

        self.assertEqual(short_url, duplicate_short_url)
        self.assertEqual(URL.objects.filter(original_url=original_url).count(), 1)


@patch('mongoengine.connection.MongoClient', new=mongomock.MongoClient)
class RedirectViewTestCase(TestCase):

    def setUp(self):
        mongoengine.connect('testdb', mongo_client_class=mongomock.MongoClient)
        URL.drop_collection()

    def _fixture_teardown(self):
        pass


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
