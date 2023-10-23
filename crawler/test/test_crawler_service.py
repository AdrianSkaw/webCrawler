import unittest
from bs4 import BeautifulSoup
from requests.models import Response
from unittest.mock import Mock, patch
from crawler.service.crawler_service import CrawlerService
from rest_framework.test import APIClient
from django.urls import reverse
from django.test import TestCase


class TestCrawlerService(TestCase):

    def setUp(self):
        self.__crawler = CrawlerService()
        self.__client = APIClient()
        self.__url = reverse('crawler')

    def test_get_attribute(self):
        element_html = '<div class="product" data-price="100">Product Name</div>'
        attribute = self.__crawler.get_attribute(element_html, 'div.product', 'data-price')
        self.assertEqual(attribute, '100')

    def test_find_elements(self):
        web_session = BeautifulSoup('<html><div class="item">Item 1</div><div class="item">Item 2</div></html>',
                                    'html.parser')
        elements = self.__crawler.find_elements(web_session, 'div.item')
        self.assertEqual(len(elements), 2)

    def test_get_text(self):
        element_html = '<div class="product">Product Name</div>'
        text = self.__crawler.get_text(element_html, 'div.product')
        self.assertEqual(text, 'Product Name')

    def test_get_text_with_missing_element(self):
        element_html = '<div class="product"></div>'
        text = self.__crawler.get_text(element_html, 'div.product', allow_missing=True)
        self.assertIsNone(text)

    def test_create_web_session(self):
        with patch('requests.get') as mock_get:
            mock_response = Mock(spec=Response)
            mock_response.status_code = 200
            mock_response.text = '<html><title>Sample Page</title></html>'
            mock_get.return_value = mock_response
            web_session = self.__crawler.create_web_session('http://example.com')
            self.assertIsInstance(web_session, BeautifulSoup)
            title = web_session.find('title').text
            self.assertEqual(title, 'Sample Page')

    @patch('requests.get')
    def test_create_web_session_with_error(self, mock_get):
        mock_response = Mock(spec=Response)
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        with self.assertRaises(Exception):
            self.__crawler.create_web_session('http://example.com')

    def test_crawl(self):
        payload = {
            'url': 'http://example.com',
            'list_selector': 'div.item',
            'selectors': {
                'title': 'div.title',
                'price': 'div.price'
            },
            'config': {
                'title': {'allow_missing': False},
                'price': {'allow_missing': True}
            }
        }
        with patch('requests.get') as mock_get:
            mock_response = Mock(spec=Response)
            mock_response.status_code = 200
            mock_response.text = '<html><div class="item" href="http://domena.com"><div class="title">Product 1</div><div class="price">100</div></div><div class="item"><div class="title">Product 2</div></div></html>'
            mock_get.return_value = mock_response
            request_data = Mock(**payload)
            result = self.__crawler.crawl(request_data)
            expected_result = [
                {'title': 'Product 1', 'price': '100'},
                {'title': 'Product 2', 'price': None}
            ]
            self.assertEqual(result, expected_result)

    def test_crawl_controller_except_200(self):
        payload = {
            'url': 'http://example.com',
            'list_selector': 'div.item',
            'selectors': {
                'title': 'div.title',
                'price': 'div.price'
            },
            'config': {
                'title': {'allow_missing': False},
                'price': {'allow_missing': True}
            }
        }
        response = self.__client.post(self.__url, payload, format='json')
        self.assertEqual(response.status_code, 200)

    def test_crawl_controller_missing_payload_fields(self):
        payload = {
            'list_selector': 'div.item',
            'selectors': {
                'title': 'div.title',
                'price': 'div.price'
            },
            'config': {
                'title': {'allow_missing': False},
                'price': {'allow_missing': True}
            }
        }
        response = self.__client.post(self.__url, payload, format='json')
        response_expected = b'["Missing field key in request data"]'
        self.assertContains(response, response_expected, status_code=400)

    def test_crawl_config_keys_not_equal_selectors_keys(self):
        payload = {
            'url': 'http://example.com',
            'list_selector': 'div.item',
            'selectors': {
                'title': 'div.title',
                'price': 'div.price'
            },
            'config': {
                'title': {'allow_missing': False}
            }
        }
        url = 'http://127.0.0.1:8000/api/v1/crawler'
        response = self.__client.post(url, payload, format='json')
        response_expected = b'["Invalid value - the \\"config\\" field is missing required fields"]'
        self.assertContains(response, response_expected, status_code=400)


if __name__ == '__main__':
    unittest.main()
