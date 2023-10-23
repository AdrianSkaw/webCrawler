from abc import ABC
from bs4 import BeautifulSoup
import requests

from crawler.service.crawler_interface import CrawlerInterface


class CrawlerService(CrawlerInterface, ABC):

    def get_attribute(self, element_html, xpath_price, attribute) -> str:
        """
        Get an attribute from an HTML element.
        """
        element_soup = BeautifulSoup(str(element_html), 'html.parser')
        single_element = element_soup.select(xpath_price)
        if single_element and attribute in single_element[0].attrs:
            return single_element[0].attrs[attribute]
        else:
            return ""

    def find_elements(self, web_session, xpath):
        """
        Find elements using the provided selector.
        """
        return web_session.select(xpath)

    def get_text(self, element_html, xpath, allow_missing=False):
        """
        Get text from an HTML element based on the selector.
        If 'allow_missing' is set to True, it returns None if the element does not exist.
        """
        element_soup = BeautifulSoup(str(element_html), 'html.parser')
        single_element = element_soup.select(xpath)
        if not single_element:
            if allow_missing:
                return None
            raise Exception(f"Element not found for xpath: {xpath}")
        text = single_element[0].next
        if not text:
            if allow_missing:
                return None
            raise Exception(f"Text not found for xpath: {xpath}")
        return text

    def create_web_session(self, url, headers=None):
        """
        Create a web session and return it as a BeautifulSoup object.
        """
        if not headers:
            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0"
            }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return BeautifulSoup(response.text, 'html.parser')
        else:
            raise Exception(f"Failed to fetch the page: {url}. Status code: {response.status_code}")

    def crawl(self, request_data):
        """
        Process a web scraping request.
        """

        url = request_data.url
        headers = request_data.headers
        web_session = self.create_web_session(url, headers)

        xpath = request_data.list_selector
        elements = self.find_elements(web_session, xpath)
        output = []
        selectors = request_data.selectors
        config = request_data.config

        for element_html in elements:
            product = {}
            for key, xpath in selectors.items():
                allow_missing = config.get(key).get('allow_missing', False)
                selector_type = config.get(key).get('attribute', 'text')
                if selector_type == 'text':
                    product[key] = self.get_text(element_html, xpath, allow_missing)
                else:
                    attribute_data = self.get_attribute(element_html, xpath, selector_type)
                    if selector_type == 'href':
                        if attribute_data.startswith('http'):
                            product['url'] = attribute_data
                        else:
                            start_url = url.rsplit('/', 3)
                            product['url'] = start_url[0] + attribute_data
            output.append(product)
        return output
