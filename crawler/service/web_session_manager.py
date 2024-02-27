import requests
from bs4 import BeautifulSoup
from rest_framework import serializers


class WebSessionManager:
    @staticmethod
    def create_web_session(url: str, headers: dict = None) -> BeautifulSoup:
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
        if response.status_code != 200:
            raise serializers.ValidationError(f"Failed to fetch the page: {url}. Status code: {response.status_code}")
        return BeautifulSoup(response.text, 'html.parser')


