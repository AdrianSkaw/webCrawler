import unittest
from bs4 import BeautifulSoup
from requests.models import Response
from unittest.mock import Mock
from unittest.mock import patch

from django.test import TestCase

from crawler.service.html_parser import HTMLParser
from crawler.service.web_session_manager import WebSessionManager


class TestCrawlerService(TestCase):

    def test_get_attribute(self):
        parser = HTMLParser()
        element_html = '<div class="product" data-price="100">Product Name</div>'
        attribute = parser.get_attribute(element_html, 'div.product', 'data-price')
        self.assertEqual(attribute, '100')

    def test_find_elements(self):
        parser = HTMLParser()
        web_session = BeautifulSoup('<html><div class="item">Item 1</div><div class="item">Item 2</div></html>',
                                    'html.parser')
        elements = parser.find_elements(web_session, 'div.item')
        self.assertEqual(len(elements), 2)

    def test_get_text(self):
        parser = HTMLParser()
        element_html = '<div class="product">Product Name</div>'
        text = parser.get_text(element_html, 'div.product')
        self.assertEqual(text, 'Product Name')

    def test_get_text_with_missing_element(self):
        parser = HTMLParser()
        element_html = '<div class="product"></div>'
        text = parser.get_text(element_html, 'div.product', allow_missing=True)
        self.assertIsNone(text)

    def test_create_web_session(self):
        with patch('requests.get') as mock_get:
            mock_response = Mock(spec=Response)
            mock_response.status_code = 200
            mock_response.text = '<html><title>Sample Page</title></html>'
            mock_get.return_value = mock_response
            web_session = WebSessionManager.create_web_session('http://example.com')
            self.assertIsInstance(web_session, BeautifulSoup)
            title = web_session.find('title').text
            self.assertEqual(title, 'Sample Page')

    @patch('requests.get')
    def test_create_web_session_with_error(self, mock_get):
        mock_response = Mock(spec=Response)
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        with self.assertRaises(Exception):
            WebSessionManager.create_web_session('http://example.com')


if __name__ == '__main__':
    unittest.main()
