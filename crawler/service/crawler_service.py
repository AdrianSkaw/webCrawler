import re
from typing import Union, Type

from crawler.service.dto.request_data import RequestData
from crawler.repository import BrandRepository, BrandDetailsRepository
from crawler.service.html_parser import HTMLParser
from crawler.service.web_session_manager import WebSessionManager


class CrawlerService:

    def __init__(self, parser: Type[HTMLParser], web_session_manager: Type[WebSessionManager]):
        self.parser = parser
        self.web_session_manager = web_session_manager

    def __crawl_category(self, request_data: RequestData) -> list:

        web_session = self.web_session_manager.create_web_session(request_data.url, request_data.headers)
        elements = self.parser.find_elements(web_session, request_data.list_selector)
        output = []
        for element_html in elements:
            product = self.__process_element(element_html, request_data)
            output.append(product)
            self.__save_to_db(product)

        return output

    @staticmethod
    def __save_to_db(product):
        product['price'] = CrawlerService.__normalize_price_to_float_format(product['price'])
        if BrandRepository.is_exist(product):
            brand = BrandRepository.get_by_name(name=product.get("title"))
        else:
            brand = BrandRepository.create(product)
        BrandDetailsRepository.create(brand, product)

    @staticmethod
    def __normalize_price_to_float_format(price):
        return float(CrawlerService.__normalize_price(price))
    @staticmethod
    def __normalize_price(price_str):
        return re.sub("[^0-9.,-]", "", price_str).replace(",", ".")

    def __process_element(self, element_html: str, request_data: RequestData) -> dict[str, Union[str, None]]:
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
        return self.parser.get_text(element_html_str, xpath, allow_missing)

    def __extract_attribute(self, element_html_str: str, xpath: str, selector_type: str) -> Union[str, None]:
        return self.parser.get_attribute(element_html_str, xpath, selector_type)

    @staticmethod
    def __process_href(attribute_data: str, product: dict[str, Union[str, None]], request_data: RequestData):
        if attribute_data and attribute_data.startswith('http'):
            product['url'] = attribute_data
        else:
            start_url_parts = request_data.url.rsplit('/', 3)
            product['url'] = start_url_parts[0] + attribute_data

    def crawl(self, request_data: RequestData) -> list:

        output = self.__crawl_category(request_data)
        return output
