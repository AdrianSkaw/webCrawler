from typing import Union

from bs4 import BeautifulSoup
from rest_framework import serializers


class HTMLParser:
    @staticmethod
    def get_attribute(element_html: str, xpath_price: str, attribute: str) -> Union[str, None]:
        """
        Get an attribute from an HTML element.
        """
        element_soup = BeautifulSoup(element_html, 'html.parser')
        single_element = element_soup.select(xpath_price)
        if single_element and attribute in single_element[0].attrs:
            return single_element[0].attrs[attribute]
        else:
            return None

    @staticmethod
    def find_elements(web_session: BeautifulSoup, xpath: str) -> list:
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

    @staticmethod
    def get_text(element_html: str, xpath: str, allow_missing: bool = False) -> Union[str, None]:
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
        return text.strip()
