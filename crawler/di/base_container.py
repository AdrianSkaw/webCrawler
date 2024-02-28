from dependency_injector import containers, providers

from crawler.service.crawler_service import CrawlerService
from crawler.service.html_parser import HTMLParser
from crawler.service.web_session_manager import WebSessionManager
from crawler.validator.request_validator import RequestValidator


class BaseContainer(containers.DeclarativeContainer):
    request_validator = providers.Factory(RequestValidator)
    html_parser = providers.Factory(HTMLParser)
    web_session_manager = providers.Factory(WebSessionManager)
    crawler_service = providers.Factory(CrawlerService,
                                        html_parser, web_session_manager
                                        )

