from typing import Type

from .web_session_manager import WebSessionManager
from .html_parser import HTMLParser


class Crawler:
    def __init__(self, parser: Type[HTMLParser], session_manager: Type[WebSessionManager]):
        self.parser = parser
        self.session_manager = session_manager

    def crawl(self, url: str, selector: str):
        web_session = self.session_manager.create_web_session(url)
        elements = self.parser.find_elements(web_session, selector)