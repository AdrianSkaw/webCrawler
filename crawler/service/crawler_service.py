import re
from typing import Union, Type

from crawler.service.dto.request_data import RequestData
from crawler.repository import BrandRepository, BrandDetailsRepository
from crawler.service.html_parser import HTMLParser
from crawler.service.web_session_manager import WebSessionManager


class CrawlerService:

    def __init__(self, parser: HTMLParser, web_session_manager: WebSessionManager):
        self.parser = parser
        self.web_session_manager = web_session_manager

    def crawl(self, request_data: RequestData) -> list:
        """
        Process a web scraping request.

        Args:
            request_data (RequestData): The data for the web scraping request.

        Returns:
            list: A list of scraped data.
        """
        try:
            output = self.__crawl_category(request_data)
            return output
        except Exception as e:
            # Handle the exception here, e.g., logging, returning an empty list, or raising the exception further
            print(f"An error occurred while processing the request: {e}")
            return []

    def __crawl_category(self, request_data: RequestData) -> list:
        """
        Process a web scraping request for a category.

        Args:
            request_data (RequestData): The data for the web scraping request.

        Returns:
            list: A list of scraped data for the category.
        """
        web_session = self.web_session_manager.create_web_session(request_data.url, request_data.headers)
        elements = self.parser.find_elements(web_session, request_data.list_selector)
        output = []
        for element_html in elements:
            product = self.__process_element(element_html, request_data)
            output.append(product)
            self.__save_to_db(product)
        return output

    def __save_to_db(self, product):
        """
        Save product data to the database.

        Args:
            product: Product data to save.
        """
        product['price'] = self.__normalize_price_to_float_format(product['price'])
        if BrandRepository.is_exist(product):
            brand = BrandRepository.get_by_name(name=product.get("title"))
        else:
            brand = BrandRepository.create(product)
        BrandDetailsRepository.create(brand, product)

    def __normalize_price_to_float_format(self, price):
        """
        Normalize price to float format.

        Args:
            price: The price to normalize.

        Returns:
            float: The normalized price.
        """
        return float(self.__normalize_price(price))

    @staticmethod
    def __normalize_price(price_str):
        """
        Normalize the price string.

        Args:
            price_str: The price string to normalize.

        Returns:
            str: The normalized price string.
        """
        return re.sub("[^0-9.,-]", "", price_str).replace(",", ".")

    def __process_element(self, element_html: str, request_data: RequestData) -> dict[str, Union[str, None]]:
        """
        Process an HTML element.

        Args:
            element_html (str): The HTML content of the element.
            request_data (RequestData): The data for the web scraping request.

        Returns:
            dict: Processed element data.
        """
        element_html_str = str(element_html)
        product = {}
        for key, xpath in request_data.selectors.items():
            allow_missing = request_data.config.get(key, {}).get('allow_missing', False)
            selector_type = request_data.config.get(key, {}).get('attribute', 'text')
            if selector_type == 'text':
                product[key] = self.__extract_text(element_html_str, xpath, allow_missing)
            else:
                attribute_data = self.__extract_attribute(element_html_str, xpath, selector_type)
                if selector_type == 'href':
                    self.__process_href(attribute_data, product, request_data)
        return product

    def __extract_text(self, element_html_str: str, xpath: str, allow_missing: bool) -> Union[str, None]:
        """
        Extract text from an HTML element.

        Args:
            element_html_str (str): The HTML content of the element.
            xpath (str): The XPath selector for the text.
            allow_missing (bool): Whether missing text is allowed.

        Returns:
            str: Extracted text or None if not found.
        """
        return self.parser.get_text(element_html_str, xpath, allow_missing)

    def __extract_attribute(self, element_html_str: str, xpath: str, selector_type: str) -> Union[str, None]:
        """
        Extract an attribute from an HTML element.

        Args:
            element_html_str (str): The HTML content of the element.
            xpath (str): The XPath selector for the attribute.
            selector_type (str): The type of attribute to extract.

        Returns:
            str: Extracted attribute or None if not found.
        """
        return self.parser.get_attribute(element_html_str, xpath, selector_type)

    @staticmethod
    def __process_href(attribute_data: str, product: dict[str, Union[str, None]], request_data: RequestData):
        """
        Process a href attribute.

        Args:
            attribute_data (str): The href attribute value.
            product (dict): The product data.
            request_data (RequestData): The data for the web scraping request.
        """
        if attribute_data and attribute_data.startswith('http'):
            product['url'] = attribute_data
        else:
            start_url_parts = request_data.url.rsplit('/', 3)
            product['url'] = start_url_parts[0] + attribute_data
