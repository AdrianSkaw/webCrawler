from dependency_injector import containers, providers

from crawler.service.crawler_service import CrawlerService
from crawler.validator.request_validator import RequestValidator


class BaseContainer(containers.DeclarativeContainer):
    request_validator = providers.Factory(RequestValidator)
    crawler_service = providers.Factory(CrawlerService)

