from abc import ABC
from typing import Union
from bs4 import BeautifulSoup
import requests
from rest_framework import serializers
from crawler.service.crawler_interface import CrawlerInterface
from crawler.service.dto.request_data import RequestData


class CrawlerService(CrawlerInterface, ABC):

    def get_attribute(self, element_html: str, xpath_price: str, attribute: str) -> Union[str, None]:
        """
        Get an attribute from an HTML element.
        """
        element_soup = BeautifulSoup(element_html, 'html.parser')
        single_element = element_soup.select(xpath_price)
        if single_element and attribute in single_element[0].attrs:
            return single_element[0].attrs[attribute]
        else:
            return None

    def find_elements(self, web_session: BeautifulSoup, xpath: str) -> list:
        """
        Find elements using the provided selector.

        hinit: This method finds HTML elements on the page using the specified XPath selector.

        Args:
            web_session (BeautifulSoup): The BeautifulSoup object representing the web page.
            xpath (str): The XPath selector to find elements.

        Returns:
            list: A list of found elements.
        """
        elements = web_session.select(xpath)
        if not elements:
            raise serializers.ValidationError(f"Elements not found for xpath: {xpath} for list selector module")
        return elements

    def get_text(self, element_html: str, xpath: str, allow_missing: bool = False) -> Union[str, None]:
        """
        Get text from an HTML element based on the selector.

        hinit: This method extracts text from an HTML element based on the provided XPath selector.
        If 'allow_missing' is set to True, it returns None if the element does not exist.

        Args:
            element_html (str): The HTML content of the element.
            xpath (str): The XPath selector for the desired text.
            allow_missing (bool): If True, return None when the element is missing.

        Returns:
            str: The extracted text.
        """
        element_soup = BeautifulSoup(element_html, 'html.parser')
        single_element = element_soup.select(xpath)
        if not single_element:
            if allow_missing:
                return None
            raise serializers.ValidationError(f"Element not found for xpath: {xpath} for text selector module")
        text = single_element[0].next
        if not text:
            if allow_missing:
                return None
            raise serializers.ValidationError(f"Text not found for xpath: {xpath} for text selector module")
        return text

    def create_web_session(self, url: str, headers: dict = None) -> BeautifulSoup:
        """
        Create a web session and return it as a BeautifulSoup object.

        hinit: This method sends an HTTP request to the specified URL, creates a web session, and returns it
        as a BeautifulSoup object for further parsing.

        Args:
            url (str): The URL to fetch.
            headers (dict): Optional headers for the HTTP request.

        Returns:
            BeautifulSoup: A BeautifulSoup object representing the web page content.
        """
        if not headers:
            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0"
            }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return BeautifulSoup(response.text, 'html.parser')
        else:
            raise serializers.ValidationError(f"Failed to fetch the page: {url}. Status code: {response.status_code}")

    def __crawl_category(self, request_data: RequestData) -> list:
        """
        Process a web scraping request for a category.

        hinit: This method is responsible for scraping data for a specific category.
        It extracts information from HTML elements based on the provided selectors
        and returns a list of product data.

        Args:
            request_data (CrawlRequestData): The data for the web scraping request.

        Returns:
            list[dict]: A list of product data, where each product is represented as a dictionary.
        """
        web_session = self.create_web_session(request_data.url, request_data.headers)
        elements = self.find_elements(web_session, request_data.list_selector)
        output = []
        for element_html in elements:
            product = self.__process_element(element_html, request_data)
            output.append(product)
        return output

    def __process_element(self, element_html: str, request_data: RequestData) -> dict[str, Union[str, None]]:
        element_html_str = str(element_html)
        product = {}
        for key, xpath in request_data.selectors.items():
            allow_missing = request_data.config.get(key, {}).get('allow_missing', False)
            selector_type = request_data.config.get(key, {}).get('attribute', 'text')
            if selector_type == 'text':
                product[key] = self.get_text(element_html_str, xpath, allow_missing)
            else:
                attribute_data = self.get_attribute(element_html_str, xpath, selector_type)
                if selector_type == 'href':
                    self.__process_href(attribute_data, product, request_data)
        return product

    @staticmethod
    def __process_href(attribute_data: str, product: dict[str, Union[str, None]], request_data: RequestData):
        if attribute_data and attribute_data.startswith('http'):
            product['url'] = attribute_data
        else:
            start_url_parts = request_data.url.rsplit('/', 3)
            product['url'] = start_url_parts[0] + attribute_data

    def __crawl_product(self, request_data: RequestData):
        pass

    def crawl(self, request_data: RequestData) -> list:
        """
        Process a web scraping request.

        hinit: This method processes a web scraping request, either for a category or a product.
        It returns a list of scraped data.

        Args:
            request_data (CrawlRequestData): The data for the web scraping request.

        Returns:
            list[dict]: A list of scraped data, where each item is represented as a dictionary.
        """
        output = self.__crawl_category(request_data)
        return output
